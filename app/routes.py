from collections import deque
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .monitor import get_history, get_state, start_monitor, trigger_demo_alert

bp = Blueprint('main', __name__)
start_monitor()

alerts = deque(maxlen=100)


def _normalize_alert_timestamp(value):
    # Alertmanager uses the Go zero timestamp for an unresolved firing alert end time.
    if not value or str(value).startswith('0001-01-01'):
        return None
    return value

@bp.route('/')
def dashboard():
    return render_template('dashboard.html')

@bp.route('/api/status')
def api_status():
    return jsonify(get_state())

@bp.route('/api/history')
def api_history():
    return jsonify(get_history())

@bp.route('/api/alerts')
def api_alerts():
    return jsonify(list(alerts))

@bp.route('/webhook/alertmanager', methods=['POST'])
def alertmanager_webhook():
    payload = request.get_json(silent=True) or {}
    received_at = datetime.now(timezone.utc).isoformat()

    for item in payload.get('alerts', []):
        alerts.appendleft({
            'received_at': received_at,
            'status': item.get('status', 'unknown'),
            'labels': item.get('labels', {}),
            'annotations': item.get('annotations', {}),
            'startsAt': _normalize_alert_timestamp(item.get('startsAt')),
            'endsAt': _normalize_alert_timestamp(item.get('endsAt')),
        })
    return jsonify({'ok': True, 'received': len(payload.get('alerts', []))})


@bp.route('/api/demo/alert', methods=['POST'])
def api_demo_alert():
    result = trigger_demo_alert()
    result['message'] = 'Demo metric raised. Prometheus should fire the PortfolioEndToEndDemo rule after 5 seconds.'
    return jsonify(result), 202

@bp.route('/health')
def health():
    current = get_state()
    http_status = 200 if current.get('health') == 'healthy' else 503
    return jsonify({'status': current.get('health'), 'details': current}), http_status

@bp.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

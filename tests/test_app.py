from app import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.get('/health')
    assert response.status_code in (200, 503)
    data = response.get_json()
    assert 'status' in data
    assert 'details' in data


def test_metrics_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'system_cpu_usage_percent' in response.data


def test_demo_alert_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.post('/api/demo/alert')
    assert response.status_code == 202
    data = response.get_json()
    assert data['triggered'] is True
    assert data['metric'] == 'portfolio_demo_alert'


def test_alertmanager_zero_end_timestamp_is_normalized():
    app = create_app()
    client = app.test_client()
    payload = {
        'alerts': [{
            'status': 'firing',
            'labels': {'alertname': 'TestAlert'},
            'annotations': {'summary': 'test'},
            'startsAt': '2026-09-11T05:24:47Z',
            'endsAt': '0001-01-01T00:00:00Z',
        }]
    }
    response = client.post('/webhook/alertmanager', json=payload)
    assert response.status_code == 200
    alerts = client.get('/api/alerts').get_json()
    assert alerts[0]['endsAt'] is None

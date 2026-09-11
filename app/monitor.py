import os
import time
import threading
from collections import deque
from datetime import datetime, timezone

import psutil
from prometheus_client import Gauge, Counter

CPU_USAGE = Gauge('system_cpu_usage_percent', 'CPU usage percent')
MEMORY_USAGE = Gauge('system_memory_usage_percent', 'Memory usage percent')
DISK_USAGE = Gauge('system_disk_usage_percent', 'Disk usage percent')
APP_HEALTH = Gauge('app_health_status', 'Application health status: 1 healthy, 0 unhealthy')
EVENTS_TOTAL = Counter('monitor_events_total', 'Total monitoring cycles completed')
DEMO_ALERT = Gauge('portfolio_demo_alert', 'Portfolio end-to-end demo alert trigger: 1 active, 0 inactive')

state = {
    'cpu': 0.0,
    'memory': 0.0,
    'disk': 0.0,
    'health': 'healthy',
    'last_updated': None,
}

history = deque(maxlen=60)
_lock = threading.Lock()
_started = False
_demo_timer = None


def collect_once():
    cpu = round(psutil.cpu_percent(interval=None), 1)
    memory = round(psutil.virtual_memory().percent, 1)
    disk = round(psutil.disk_usage('/').percent, 1)

    # Health rule is intentionally simple and transparent for portfolio/demo use.
    health = 'healthy' if cpu < 90 and memory < 90 and disk < 95 else 'degraded'

    CPU_USAGE.set(cpu)
    MEMORY_USAGE.set(memory)
    DISK_USAGE.set(disk)
    APP_HEALTH.set(1 if health == 'healthy' else 0)
    EVENTS_TOTAL.inc()

    snapshot = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'cpu': cpu,
        'memory': memory,
        'disk': disk,
        'health': health,
    }

    with _lock:
        state.update(snapshot)
        state['last_updated'] = snapshot['timestamp']
        history.append(snapshot)


def monitor_loop(interval=2):
    while True:
        collect_once()
        time.sleep(interval)


def _configured_monitor_interval(default=2.0):
    raw = os.getenv('MONITOR_INTERVAL_SECONDS', str(default))
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return default
    return max(value, 0.5)


def start_monitor(interval=None):
    global _started
    if _started:
        return
    _started = True
    interval = _configured_monitor_interval() if interval is None else interval
    collect_once()
    thread = threading.Thread(target=monitor_loop, args=(interval,), daemon=True)
    thread.start()


def get_state():
    with _lock:
        return dict(state)


def get_history():
    with _lock:
        return list(history)


def trigger_demo_alert(duration=20):
    """Raise a safe portfolio-only Prometheus gauge and reset it automatically."""
    global _demo_timer
    DEMO_ALERT.set(1)
    if _demo_timer is not None:
        _demo_timer.cancel()
    _demo_timer = threading.Timer(duration, lambda: DEMO_ALERT.set(0))
    _demo_timer.daemon = True
    _demo_timer.start()
    return {
        'triggered': True,
        'metric': 'portfolio_demo_alert',
        'value': 1,
        'auto_reset_seconds': duration,
    }

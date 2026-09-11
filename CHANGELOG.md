# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project follows [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-09-11

### Added
- Safe end-to-end alert demo exposed through `POST /api/demo/alert` and the dashboard.
- Dedicated `PortfolioEndToEndDemo` Prometheus alert rule.
- Alert lifecycle visibility for `firing` and `resolved` notifications.
- Normalization of Alertmanager's Go zero `endsAt` timestamp to `null` in the API.
- Automated tests for the demo endpoint and Alertmanager timestamp normalization.
- Reproducible Prometheus and Alertmanager image versions in Docker Compose.
- GitHub documentation, architecture notes, screenshots, MIT license, and CI workflow.
- Configurable metric sampling interval through `MONITOR_INTERVAL_SECONDS`.

### Changed
- Production dependencies and development/test dependencies are separated into
  `requirements.txt` and `requirements-dev.txt`.
- `.gitignore` and `.dockerignore` expanded for a cleaner public repository and
  smaller Docker build context.
- Direct webhook testing and the true end-to-end demo are now clearly separated
  into distinct scripts and Make targets.
- Removed the unused `requests` runtime dependency.

## [1.0.0] - 2026-09-11

### Added
- Flask monitoring service with CPU, memory, disk, and application-health metrics.
- Prometheus `/metrics` endpoint and alert rules.
- Alertmanager webhook routing back to the Flask application.
- Real-time dashboard with recent metric history and alert activity.
- Health, status, history, alerts, and metrics endpoints.
- Docker Compose deployment for the application, Prometheus, and Alertmanager.
- Initial automated endpoint tests.

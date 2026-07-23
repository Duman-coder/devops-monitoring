# DevOps Monitoring Platform

Система мониторинга сети построенная на современном DevOps стеке.

## Стек технологий

- **Python** — скрипт мониторинга (ping check)
- **Docker + Docker Compose** — контейнеризация
- **Prometheus** — сбор метрик
- **Grafana** — визуализация и дашборды
- **Nginx** — reverse proxy
- **GitHub Actions** — CI/CD пайплайн

## Быстрый старт

```bash
git clone https://github.com/Duman-coder/devops-monitoring
cd devops-monitoring
docker compose up -d
```

Открой в браузере:
- Grafana: http://localhost (admin/admin123)
- Prometheus: http://localhost/prometheus

## Автор

Duman | Network Engineer → DevOps Engineer

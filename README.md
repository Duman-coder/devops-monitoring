# 🔍 DevOps Monitoring Platform

![CI](https://github.com/Duman-coder/devops-monitoring/actions/workflows/ci.yml/badge.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-ready-326CE5?logo=kubernetes)
![Python](https://img.shields.io/badge/Python-3.11-green?logo=python)
![Prometheus](https://img.shields.io/badge/Prometheus-monitoring-E6522C?logo=prometheus)
![Grafana](https://img.shields.io/badge/Grafana-dashboards-F46800?logo=grafana)

Система мониторинга сети построенная на современном DevOps стеке.
Автоматически проверяет доступность хостов, собирает метрики и визуализирует данные.

---

## 🏗️ Архитектура
ping-monitor (Python)
↓
Docker Compose / Kubernetes
↓
Prometheus (метрики) → Grafana (дашборды)
↓
Nginx (reverse proxy)

## 🛠️ Стек технологий

| Технология | Использование |
|---|---|
| Python 3.11 | Скрипт мониторинга (ping check) |
| Docker | Контейнеризация всех сервисов |
| Docker Compose | Локальный запуск стека |
| Kubernetes | Оркестрация в продакшене |
| Prometheus | Сбор и хранение метрик |
| Grafana | Визуализация и дашборды |
| Nginx | Reverse proxy и балансировка |
| GitHub Actions | CI/CD пайплайн |

## 🚀 Быстрый старт

### Через Docker Compose

```bash
git clone https://github.com/Duman-coder/devops-monitoring
cd devops-monitoring
docker compose up -d
```

Открой в браузере:
- **Grafana:** http://localhost (admin / admin123)
- **Prometheus:** http://localhost/prometheus

### Через Kubernetes

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get all -n monitoring
```

## 📁 Структура проекта

devops-monitoring/
├── app/
│ ├── ping_check.py # Python скрипт мониторинга
│ ├── Dockerfile # Контейнеризация
│ ├── hosts.txt # Список хостов для мониторинга
│ └── requirements.txt # Python зависимости
├── k8s/
│ ├── namespace.yaml # K8s namespace
│ ├── configmap.yaml # Конфигурация
│ ├── deployment.yaml # Деплоймент
│ └── service.yaml # Сервис
├── prometheus/
│ └── prometheus.yml # Конфиг Prometheus
├── nginx/
│ └── nginx.conf # Конфиг Nginx
├── .github/workflows/
│ └── ci.yml # GitHub Actions CI/CD
└── docker-compose.yml # Оркестрация сервисов

## ⚙️ Конфигурация

Список хостов для мониторинга в файле `app/hosts.txt`:
8.8.8.8
1.1.1.1
google.com
github.com

Интервал проверки задаётся через переменную окружения:

```bash
CHECK_INTERVAL=30  # секунды
```

## 👤 Автор

**Duman** — Network Engineer → DevOps Engineer

- GitHub: [@Duman-coder](https://github.com/Duman-coder)
- Стек: Linux, Python, Docker, Kubernetes, Terraform, Ansible, Prometheus, Grafana, Vault, Nginx, ELK

## Helm — Деплой в Kubernetes

Helm чарт для деплоя ping-monitor в Kubernetes.

### Установка

\`\`\`bash
eval \$(minikube docker-env)
docker build -t ping-monitor:latest ./app
helm install ping-monitor ./helm/ping-monitor
helm list
kubectl get pods
\`\`\`

### Обновление

\`\`\`bash
helm upgrade ping-monitor ./helm/ping-monitor
\`\`\`

### Удаление

\`\`\`bash
helm uninstall ping-monitor
\`\`\`

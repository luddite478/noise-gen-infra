source ../../secrets/.env

PREFECT_K8S_NAMESPACE="prefect"

# Setup helm chart
helm repo add prefect https://prefecthq.github.io/prefect-helm
helm repo update
kubectl create namespace prefect
kubectl apply -f "api-key.yaml"
helm upgrade --install prefect-worker prefect/prefect-worker -n $PREFECT_K8S_NAMESPACE -f "values2.yaml"

kubectl create secret docker-registry dockerhub-registry-secret \
    --docker-server="$DOCKERHUB_REGISTRY_SERVER" \
    --docker-username="$DOCKERHUB_REGISTRY_USER" \
    --docker-password="$DOCKERHUB_REGISTRY_PASSWORD" \
    --namespace="$PREFECT_K8S_NAMESPACE"


set -e

PREFECT_NAMESPACE="prefect"

# Setup helm chart
helm repo add prefect https://prefecthq.github.io/prefect-helm
helm repo update
kubectl create namespace $PREFECT_NAMESPACE
kubectl apply -f "api-key.yaml"
helm upgrade --install prefect-worker prefect/prefect-worker -n $PREFECT_NAMESPACE -f "values.yaml"

kubectl create secret docker-registry dockerhub-registry-secret \
    --docker-server="$DOCKERHUB_REGISTRY_SERVER" \
    --docker-username="$DOCKERHUB_REGISTRY_USER" \
    --docker-password="$DOCKERHUB_REGISTRY_PASSWORD" \
    --namespace="$PREFECT_NAMESPACE"


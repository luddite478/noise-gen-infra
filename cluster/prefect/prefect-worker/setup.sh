helm repo add prefect https://prefecthq.github.io/prefect-helm
#helm repo update
kubectl create namespace prefect
kubectl apply -f api-key.yaml
helm install prefect-worker prefect/prefect-worker --namespace=prefect -f values.yaml

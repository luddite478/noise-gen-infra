set -e

kubectl create ns minio
kubectl apply -f volume.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml

kubectl wait --namespace minio \
  --for=condition=ready pod \
  --selector=app=minio \
  --timeout=90s

kubectl apply -f init-job.yaml


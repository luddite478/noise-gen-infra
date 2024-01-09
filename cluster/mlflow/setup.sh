helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo update

helm upgrade --install mlflow community-charts/mlflow \
  -n mlflow \
  --create-namespace \
  --set artifactRoot.s3.enabled=true \
  --set artifactRoot.s3.bucket=mlflow \
  --set artifactRoot.s3.awsAccessKeyId=minio \
  --set artifactRoot.s3.awsSecretAccessKey=minio123 \
  --set extraEnvVars.MLFLOW_S3_ENDPOINT_URL=http://minio.minio:9000 \
  --set serviceMonitor.enabled=true

kubectl apply -f inress.yaml
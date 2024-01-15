set -e

if ! command -v envsubst &> /dev/null
then
    echo "envsubst could not be found"
    exit 1
fi

helm repo add cnpg https://cloudnative-pg.github.io/charts
helm upgrade --install cnpg --namespace db-operator --create-namespace cnpg/cloudnative-pg
sleep 150
export POSTGRES_USER=$POSTGRES_USER
export POSTGRES_DB=$POSTGRES_DB
export S3_ACCESS_KEY_BASE64=$(echo -n "$S3_ACCESS_KEY" | base64)
export S3_SECRET_KEY_BASE64=$(echo -n "$S3_SECRET_KEY" | base64)
export POSTGRES_ROOT_PASSWORD_BASE64=$(echo -n "$POSTGRES_ROOT_PASSWORD" | base64)
export POSTGRES_ROOT_USER_BASE64=$(echo -n "$POSTGRES_ROOT_USER" | base64)
export POSTGRES_PASSWORD_BASE64=$(echo -n "$POSTGRES_PASSWORD" | base64)
export POSTGRES_USER_BASE64=$(echo -n "$POSTGRES_USER" | base64)

kubectl create ns db || true
envsubst < superuser.yaml | kubectl apply -f -
envsubst < user.yaml | kubectl apply -f -
envsubst < s3_creds.yaml | kubectl apply -f -
envsubst < cluster.yaml
envsubst < cluster.yaml | kubectl apply -f -

kubectl get cluster -n db
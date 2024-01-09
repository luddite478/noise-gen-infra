#!/bin/bash
set -e

source ../bin/activate

# fix line endings (windows/linux issue)
dos2unix secrets/.cluster.local.env

# export all env vars
set -a
source secrets/.cluster.local.env
set +a

cd scripts

# upload cluster config
./upload_cluster_config.sh

# create cluster
./create_cluster.sh

# download k8s config
./download_kubeconf.sh

# modify kubeconfig
pip install pyyaml python-dotenv > /dev/null
python modify_kubeconfig.py

# merge kubeconfigs
./merge_kubeconfs.sh
chmod go-r ~/.kube/config

cd -

# verify cluster access
kubectl get namespace

# setup ingress
cd ingress
./setup.sh
cd -

# setup prefect-worker
cd prefect/prefect-worker
./setup.sh
cd -

# setup minio
cd minio
./setup.sh
cd -

# setup mlflow
cd mlflow
./setup.sh
cd -





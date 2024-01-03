#!/bin/bash
set -e
# rm possible \r char in .env
tr -d '\r' < .cluster.local.env > .cluster.local.env.new
mv .cluster.local.env.new .cluster.local.env
source .cluster.local.env
# # export LOCAL_ENV_FILE_ABS_PATH="$(pwd)/.cluster.local.env.new"

# upload cluster config
./scripts/upload_cluster_config.sh

# create cluster
./scripts/create_cluster.sh

# download k8s config
./scripts/download_kubeconf.sh

# modify kubeconfig
source ../bin/activate    
pip install pyyaml python-dotenv > /dev/null
python ./scripts/modify_kubeconfig.py

# merge kubeconfigs
./scripts/merge_kubeconfs.sh

# verify cluster access
kubectl get namespace

#setup ingress
./ingress/setup.sh

#setup prefect-worker
./prefect/prefect-worker/setup.sh





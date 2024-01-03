#!/bin/bash

source .cluster.local.env

export CLUSTER_CONFIG_REMOTE_PATH="$CLUSTER_CONFIG_PATH/kind-cluster.yaml"
CREATE_CLUSTER_CMD="sshpass -p $SSH_PASSWORD ssh $SERVER_USER@$SERVER_HOST 'kind create cluster --name noise-learn --config $CLUSTER_CONFIG_REMOTE_PATH'"
eval $CREATE_CLUSTER_CMD
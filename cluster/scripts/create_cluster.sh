#!/bin/bash
CREATE_CLUSTER_CMD="sshpass -p $SSH_PASSWORD ssh $SERVER_USER@$SERVER_HOST 'kind create cluster --name noise-gen --config $CLUSTER_CONFIG_HOST_PATH'"
eval $CREATE_CLUSTER_CMD
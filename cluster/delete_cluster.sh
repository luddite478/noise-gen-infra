#!/bin/bash

source secrets/.cluster.local.env

DELETE_CLUSTER_CMD="sshpass -p $SSH_PASSWORD ssh $SERVER_USER@$SERVER_HOST 'kind delete cluster --name noise-gen'"
eval "$DELETE_CLUSTER_CMD"
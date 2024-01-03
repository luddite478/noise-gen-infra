#!/bin/bash

# rm possible \r char in .env
tr -d '\r' < .cluster.local.env > .cluster.local.env.new
mv .cluster.local.env.new .cluster.local.env
source .cluster.local.env

DELETE_CLUSTER_CMD="sshpass -p $SSH_PASSWORD ssh $SERVER_USER@$SERVER_HOST 'kind delete cluster --name noise-learn'"
eval $DELETE_CLUSTER_CMD
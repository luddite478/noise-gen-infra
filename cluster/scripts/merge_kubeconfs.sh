echo "Deleting old context with the same name..."

kubectl config unset users.$CLUSTER_NAME
kubectl config unset clusters.$CLUSTER_NAME
kubectl config delete-context $CLUSTER_NAME || true

echo "Merging ~/.kube/config with new kubeconfig..."

export KUBECONFIG="$HOME/.kube/config:$(pwd)/$TMP_CONF_NAME"
kubectl config view --flatten  > all-in-one-kubeconfig.yaml
mv all-in-one-kubeconfig.yaml ~/.kube/config
chmod go-r ~/.kube/config
rm $TMP_CONF_NAME
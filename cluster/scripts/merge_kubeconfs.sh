source .cluster.local.env

export KUBECONFIG="$HOME/.kube/config:$(pwd)/$TMP_CONF_PATH"
kubectl config view --flatten  > all-in-one-kubeconfig.yaml
mv all-in-one-kubeconfig.yaml ~/.kube/config
rm $TMP_CONF_PATH
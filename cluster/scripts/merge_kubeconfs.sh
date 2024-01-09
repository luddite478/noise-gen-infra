
export KUBECONFIG="$HOME/.kube/config:$(pwd)/$TMP_CONF_NAME"
kubectl config view --flatten  > all-in-one-kubeconfig.yaml
mv all-in-one-kubeconfig.yaml ~/.kube/config
rm $TMP_CONF_NAME
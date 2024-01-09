import yaml
import os

def modify_yaml_file(file_path, cluster_name, server_host, cluster_port):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)

    for cluster in data.get('clusters', []):
        if 'cluster' in cluster and 'name' in cluster and cluster['name'] == cluster_name:
            cluster['cluster']['server'] = f'https://{server_host}:{cluster_port}'
            cluster['cluster'].pop('certificate-authority-data', None)
            cluster['cluster']['insecure-skip-tls-verify'] = True

    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)

if __name__ == "__main__":
    try:
        print(f'Updating kubeconfig file...')
        env = os.environ
        kubeconfig_path = env['TMP_CONF_NAME']
        modify_yaml_file(kubeconfig_path, env['CLUSTER_NAME'], env['SERVER_HOST'], env['CLUSTER_PORT'])
    except Exception as e:
        print(f'An error occurred while updating kubeconfig: {e}')
        exit(1)

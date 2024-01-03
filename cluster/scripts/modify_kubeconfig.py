import yaml
from dotenv import dotenv_values
import os

def modify_yaml_file(file_path, cluster_name, server_host, cluster_port):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    for cluster in data.get('clusters', []):
        if 'cluster' in cluster and 'name' in cluster and cluster['name'] == cluster_name:
            cluster['cluster']['server'] = f'https://{server_host}:{cluster_port}'
            cluster['cluster'].pop('certificate-authority-data', None)
            cluster['cluster']['insecure-skip-tls-verify'] = True

    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(script_dir)

    env_file_path = os.path.join(parent_dir, '.cluster.local.env')
    env = dotenv_values(env_file_path)

    kubeconfig_path = os.path.join(parent_dir, env['TMP_CONF_PATH'])
    modify_yaml_file(kubeconfig_path, env['CLUSTER_NAME'], env['SERVER_HOST'], env['CLUSTER_PORT'])

from dotenv import dotenv_values
import subprocess as sp
from os import environ, path, makedirs
import secrets

env = dotenv_values('secrets/.env')
execution_env = environ.get('EXECUTION_ENV', 'kubernetes')
if execution_env == 'local':
    data_folder = env['DATA_FOLDER_LOCAL']
elif execution_env == 'kubernetes':
    data_folder = env['DATA_FOLDER_VOLUME']
else:
    print(f'Error: env variable EXECUTION_ENV wrong value: {execution_env}')
    exit(1)

def download(items, params):
    run_name = params.get('run_name', None)
    if run_name == None:
        run_name = secrets.token_hex(4)

    download_dir = path.join(data_folder, run_name)
    if not path.exists(download_dir):
        makedirs(download_dir)

    downloaded_files = []
    for item in items:
        name = item['NAME'].replace(' ', '_')
        link = item['LINK']
        ext = ".mp3"

        output_path = path.join(download_dir, name, name + ext)

        command = [
            'yt-dlp',
            '-f', 'bestaudio/best',
            '--extract-audio',
            '--audio-format', 'mp3',
            '-o', output_path,
            link
        ]

        try:
            print(f'Downloading file {link}...')
            sp.run(command, check=True)
            print(f"File downloaded successfully to {output_path}")
            downloaded_files.append(output_path)
        except sp.CalledProcessError as e:
            print(f"Error downloading file: {e}")
    
    return downloaded_files


if __name__ == "__main__":
    # test
    items = [{'NAME': 'genocide organ - leichenlinie', 'LINK': 'https://youtu.be/4oqxZvUGXe4?si=6ql80J4T04ZYfORh'}]
    download(items)
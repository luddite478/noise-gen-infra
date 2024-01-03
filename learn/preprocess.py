from dotenv import dotenv_values
import subprocess as sp
from os import environ, path, makedirs, remove
import json

env = dotenv_values('secrets/.env')
execution_env = environ.get('EXECUTION_ENV', 'kubernetes')
if execution_env == 'local':
    data_folder = env['DATA_FOLDER_LOCAL']
elif execution_env == 'kubernetes':
    data_folder = env['DATA_FOLDER_VOLUME']
else:
    print(f'Error: env variable EXECUTION_ENV wrong value: {execution_env}')
    exit(1)

def convert_to_wav_if_necessary(f_path):
    if is_wav(f_path):
        return f_path

    output_folder = path.dirname(f_path)
    no_ext_name = path.splitext(path.basename(f_path))[0]   
    wav_path = path.join(output_folder, no_ext_name + '.wav')

    command = [
        'ffmpeg',
        '-hide_banner',
        '-i', f_path,
        '-y',
        wav_path
    ]

    try:
        print(f'Converting {f_path} to wav...')
        sp.run(command, check=True)
        remove(f_path)
        return wav_path
    except sp.CalledProcessError as e:
        print(f"Error preprocessing file: {e}")
        return None

def mix_down_if_necessary(f_path):
    if get_number_of_channels(f_path) is 1:
        return f_path

    output_folder = path.dirname(f_path)
    no_ext_name = path.splitext(path.basename(f_path))[0]
    one_chan_path = path.join(output_folder, f'{no_ext_name}_1_chan.wav')

    command = [
        'ffmpeg',
        '-hide_banner',
        '-i', f_path,
        '-ac', '1',
        '-y',
        one_chan_path
    ]
    try:
        print(f'Mixing down {f_path} to 1-channel...')
        sp.run(command, check=True)
        remove(f_path)
        return one_chan_path
    except sp.CalledProcessError as e:
        print(f"Error mixing down: {e}")
        return None
    
def resample_if_necessary(f_path, sample_rate):

    if is_wav_with_sample_rate(f_path, sample_rate):
        return f_path

    output_folder = path.dirname(f_path)
    no_ext_name = path.splitext(path.basename(f_path))[0]
    resampled_path = path.join(output_folder, f'{no_ext_name}_{sample_rate}.wav')
    command = [
        'ffmpeg',
        '-hide_banner',
        '-i', f_path,
        '-ar', str(sample_rate),
        '-y',
        resampled_path
    ]

    try:
        print(f'Resampling {f_path} to {sample_rate}hz...')
        sp.run(command, check=True)
        remove(f_path)
        return resampled_path
    except sp.CalledProcessError as e:
        print(f"Error mixing down: {e}")
        return None
    
def is_wav_with_sample_rate(file_path, target_sample_rate):
    cmd = [
        'ffprobe',
        '-v', 'error',         
        '-select_streams', 'a:0',  
        '-show_entries', 'stream=codec_name,sample_rate',
        '-of', 'json',
        file_path
    ]
    
    result = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    
    try:
        output = json.loads(result.stdout.decode('utf-8'))
        codec_name = output['streams'][0]['codec_name']
        sample_rate = int(output['streams'][0]['sample_rate'])

        if codec_name.lower() == 'wav' and sample_rate == target_sample_rate:
            return True
        else:
            return False
    except (json.JSONDecodeError, KeyError, IndexError):
        return False
    
def is_wav(file_path):
    cmd = [
        'ffprobe',
        '-v', 'error',         
        '-select_streams', 'a:0',  
        '-show_entries', 'stream=codec_name,sample_rate',
        '-of', 'json',
        file_path
    ]
    
    result = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    
    try:
        output = json.loads(result.stdout.decode('utf-8'))
        codec_name = output['streams'][0]['codec_name']
        sample_rate = int(output['streams'][0]['sample_rate'])

        if codec_name.lower() == 'wav':
            return True
        else:
            return False
    except (json.JSONDecodeError, KeyError, IndexError):
        return False

def get_number_of_channels(file_path):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'a:0',  
        '-show_entries', 'stream=channels',
        '-of', 'json',
        file_path
    ]
    
    result = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    
    try:
        output = json.loads(result.stdout.decode('utf-8'))
        num_channels = output['streams'][0]['channels']
        return int(num_channels)
    except (json.JSONDecodeError, KeyError, IndexError):
        return None

# def create_processing_dir(f):
#     no_ext_name = path.splitext(path.basename(f))[0]
#     processing_dir = path.join(data_folder, run_name, 'processing', no_ext_name)
#     if not path.exists(processing_dir):
#         makedirs(processing_dir)
#     return processing_dir

def get_audio_length_in_samples(audio_path, sample_rate):
    try:
        total_samples_command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "stream=nb_samples",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]

        total_samples_output = sp.check_output(total_samples_command).decode("utf-8").strip()

        return int(total_samples_output)

    except sp.CalledProcessError as e:
        print(f"Error gettings length in samples: {e}")
        return None

def split_if_necessary(f_path, desired_length):
    print('length in samples', get_audio_length_in_samples(f_path, 48000))

def preprocess(files, params):

    preprocessed_files = []
    for f in files:
        f = convert_to_wav_if_necessary(f)
        f = resample_if_necessary(f, 48000)
        f = mix_down_if_necessary(f)
        f = split_if_necessary(f, params['audio_length'])
        
        preprocessed_files.append(f)

    # result_folder = path.join(data_folder, run_name, 'processing/result')
    # if not path.exists(result_folder):
    #     makedirs(result_folder)

        
 

if __name__ == "__main__":
    # print('Preprocessing')
    split_if_necessary('C:/projects/noise-learn/learn/data/snobbish-saluki/genocide_organ_-_leichenlinie/genocide_organ_-_leichenlinie_48000_1_chan.wav', 60)
    # preprocess(['./data/proto_vhs.wav'])
    # test
    pass
    # preprocess(items)
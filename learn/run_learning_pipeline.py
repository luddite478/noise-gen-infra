from prefect import flow, task
from prefect.context import FlowRunContext
from download   import download   as run_download
from preprocess import preprocess as run_preprocessing
# from train      import train      as run_training
# from upload     import upload     as run_upload

@task
def download(items, params):
    return run_download(items, params)

@task
def preprocess(files, params):
    run_preprocessing(files, params)
    
@task
def train():
    print("training")

@task
def upload():
    print("uploading")

@flow(log_prints=True)
def run_learning_pipeline(items, params):
    params['run_name'] = FlowRunContext.get().flow_run.dict().get('name')
    print('Items:', items)
    print('Params:', params)
    # files = download(items, params)
    # preprocess(files, params)
    # train()
    # upload()

if __name__ == "__main__":
    items = [{'NAME': 'genocide organ - leichenlinie', 'LINK': 'https://youtu.be/4oqxZvUGXe4?si=6ql80J4T04ZYfORh'}]
    params = {
        'audio_length': 60
    }
    run_learning_pipeline(items, params)
from prefect import flow
import time

@flow
def sleep():
    time.sleep(500)

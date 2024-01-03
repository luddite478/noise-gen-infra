FROM prefecthq/prefect:2-python3.11-kubernetes
COPY requirements.txt /noise-learn/requirements.txt
COPY secrets /noise-learn/secrets
RUN pip install -r requirements.txt
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import dotenv_values
from google.oauth2 import service_account
import csv
import hashlib
import time
from urllib.parse import urlparse
from prefect.client.orchestration import PrefectClient
import asyncio
import uuid

env = dotenv_values('secrets/.env')

# google_api_token = JSON.load("google-api-token")
# google_oauth_secret = JSON.load("google-oauth-secret")
# google_service_account_key = JSON.load("google-service-account-key")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = env['GOOGLE_NOISE_SPREADSHEET']
SPREADSHEET_RANGE = 'A1:B1000'
state_file = './state/audio-table.csv'

column_index_mapping = {
    'NAME': 0,
    'LINK': 1
}

allowed_link_domains = [
    "youtube.com",
    "youtu.be"
]

def get_row_hash(row):
    name = row[column_index_mapping['NAME']]

    formatted_str = ''.join(c for c in name if c.isalnum()).lower()
    
    hash_object = hashlib.sha256()
    
    hash_object.update(formatted_str.encode())
    
    hashed_str = hash_object.hexdigest()[:8]
    
    return hashed_str

def get_prev_spreadsheet_rows(state_file):
    if not os.path.exists(state_file):
        print(f'No state file found on path {state_file}')
        return []
    
    rows = []
    with open(state_file, 'r') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            rows.append(row)
    
    return rows


def google_auth():
    try:
        google_key_path = 'secrets/google-service-account-key.json'

        if not os.path.exists(google_key_path):
            print(f'No google key found on path {google_key_path}')
            raise FileNotFoundError(f'No google key found on path {google_key_path}')

        creds = service_account.Credentials.from_service_account_file(google_key_path, scopes=SCOPES)
        service = build("sheets", "v4", credentials=creds)
        return service
	
    except HttpError as err:
        print(err)
        return None

def get_spreadsheet_rows(google_service):
    try:
        sheet = google_service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SPREADSHEET_ID, range=SPREADSHEET_RANGE)
            .execute()
        )
        rows = result.get("values", [])

        if not rows:
            print("No data found.")
            return

        return rows 


    except HttpError as err:
        print(err)
        return None

def find_new_rows(now_rows, prev_rows):
    new_rows = []
    prev_hashes = [get_row_hash(r) for r in prev_rows]
    for now_row in now_rows:
        now_hash = get_row_hash(now_row)      
        if now_hash not in prev_hashes:
            new_rows.append(now_row)
    return new_rows

def save_state(rows):
    with open(state_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        
        for row in rows:
            csv_writer.writerow(row)

def is_valid_link(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        if domain in allowed_link_domains:
            return all([parsed_url.scheme, parsed_url.netloc])
        return False
    except ValueError:
        return False

def validate_rows(rows):
    validated_rows = []
    for row in rows:
        name = row[column_index_mapping['NAME']]
        link = row[column_index_mapping['LINK']]

        if name == '' or link == '':
            continue

        if is_valid_link(link):
            validated_rows.append(row)
        else:
            print(f'Row with name [{name}] and link [{link}] is not valid')
    
    return validated_rows

def rows_to_dict(table_rows, column_index_mapping):
    if not table_rows or not column_index_mapping:
        return []
    headers = list(column_index_mapping.keys())
    return [dict(zip(headers, [row[index] for _, index in column_index_mapping.items()])) for row in table_rows]

async def run_learning_pipeline(learn_args):
    '''
    learn_args: {
        'items': [{'NAME', '', 'LINK': ''}]
        'params': {}
    }
    '''
    client = PrefectClient(api=env['PREFECT_API_URL'], api_key=env['PREFECT_API_KEY'])
    dep_id = uuid.UUID(env['PREFECT_PIPELINE_DEPLOYMENT_ID'])
    
    res = await client.create_flow_run_from_deployment(deployment_id=dep_id, parameters=learn_args)
    print('Learning deployment response:', res)

def check_new_data():
    google_service = google_auth()
    
    prev_rows = get_prev_spreadsheet_rows(state_file)
    now_rows  = get_spreadsheet_rows(google_service)
    new_rows  = find_new_rows(now_rows, prev_rows)
    validated_new_rows = validate_rows(new_rows)

    if len(validated_new_rows) > 0:
        learn_args = {'items': rows_to_dict(validated_new_rows, column_index_mapping)}
        print('Found new rows:', validated_new_rows)
        print('Running learning pipeline...')
        asyncio.run(run_learning_pipeline(learn_args))
        save_state(prev_rows + validated_new_rows)

def watch_for_new_data():
    print('Started watcher')
    while True:
        check_new_data()
        time.sleep(5)

if __name__ == "__main__":
    watch_for_new_data()a




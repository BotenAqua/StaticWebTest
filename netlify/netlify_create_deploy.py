import os
import requests
import json

from netlify_json_handler import get_files_json

netlify_api_url = 'https://api.netlify.com/api/v1'

def get_vars():
    netlify_token = os.getenv('NETLIFY_API_KEY')
    netlify_site_id = os.getenv('NETLIFY_SITE_ID')
    
    if netlify_token is None:
        print('Missing NETLIFY_API_KEY, exiting...')
        exit()
    if netlify_site_id is None:
        print('Missing NETLIFY_SITE_ID, exiting...')
        exit()
    return netlify_token, netlify_site_id

def create_deploy(netlify_token, site_id, file_dict:dict):
    headers = {
        'Authorization': f'Bearer {netlify_token}',
        'Content-Type': 'application/json'
    }

    data = file_dict

    response = requests.post(f'{netlify_api_url}/sites/{site_id}/deploys', headers=headers, data=json.dumps(data))
    print(f'Create deploy - response code: {response.status_code}')
    return response.json()


if __name__ == '__main__':
    netlify_token, netlify_site_id = get_vars()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dict = get_files_json(file_location=current_dir)
    deploy = create_deploy(netlify_token, netlify_site_id, file_dict)
    print(deploy)
    print(f'Deploy created with ID: {deploy["id"]}')

import os
import requests

from netlify_json_handler import get_files_json

netlify_api_url = 'https://api.netlify.com/api/v1'

def get_vars():
    netlify_token = os.getenv('NETLIFY_API_KEY')
    netlify_site_id = os.getenv('NETLIFY_SITE_ID')
    netlify_deploy_id = os.getenv('NETLIFY_DEPLOY_ID')
    
    if netlify_token is None:
        print('Missing NETLIFY_API_KEY, exiting...')
        exit()
    if netlify_site_id is None:
        print('Missing NETLIFY_SITE_ID, exiting...')
        exit()
    if netlify_deploy_id is None:
        print('Missing NETLIFY_DEPLOY_ID, exiting...')
        exit()
    return netlify_token, netlify_site_id, netlify_deploy_id

def get_deploys(netlify_token, site_id):
    headers = {
        'Authorization': f'Bearer {netlify_token}'
    }
    
    response = requests.get(f'{netlify_api_url}/sites/{site_id}/deploys', headers=headers)
    print(f'Get DeployID - response code {response.status_code}')
    return response.json()

def upload_files(netlify_token, deploy_id, files, files_dir = 'site/'):
    failure_flag = False

    headers = {
        'Authorization': f'Bearer {netlify_token}',
        'Content-Type': 'application/octet-stream'
    }
    
    for file_path, sha in files['files'].items():
        url = f'{netlify_api_url}/deploys/{deploy_id}/files/{file_path}'
        file_dir = files_dir + file_path
        with open(file_dir, 'rb') as file:
            response = requests.put(url, headers=headers, data=file.read())
            status_code = response.status_code
            if status_code == 200:
                print(f'Uploaded {file_path}: {response.status_code}')
            else:
                print(f'Failed to upload {file_path}: {response.status_code}')
                failure_flag = True
        if failure_flag:
            print('There was at least one error on upload, exiting...')
            exit()
    return


if __name__ == '__main__':
    netlify_token, netlify_site_id, netlify_deploy_id = get_vars()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = get_files_json(file_location=current_dir)
    upload_files(netlify_token, netlify_deploy_id, files)

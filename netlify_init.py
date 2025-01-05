import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

netlify_api_url = 'https://api.netlify.com/api/v1'
netlify_token = os.getenv('NETLIFY_API_KEY')

def init_site(site_name):
    headers = {
        'Authorization': f'Bearer {netlify_token}',
        'Content-Type': 'application/json'
    }

    data = {
        'name': site_name
    }
    
    response = requests.post(f'{netlify_api_url}/sites', headers=headers, data=json.dumps(data))
    print(f'Init Site - response code {response.status_code}')
    return response.json()

def create_deploy(site_id, file_dict:dict):
    headers = {
        'Authorization': f'Bearer {netlify_token}',
        'Content-Type': 'application/json'
    }

    data = file_dict

    response = requests.post(f'{netlify_api_url}/sites/{site_id}/deploys', headers=headers, data=json.dumps(data))
    print(f'Create deploy - response code: {response.status_code}')
    return response.json()


def get_deploy_id(site_id):
    headers = {
        'Authorization': f'Bearer {netlify_token}'
    }
    
    response = requests.get(f'{netlify_api_url}/sites/{site_id}/deploys', headers=headers)
    print(f'Get DeployID - response code {response.status_code}')
    return response.json()

def upload_files(deploy_id, files):
    failure_flag = False
    files_dir = 'site/'

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
                print('Failed to upload {file_path}: {response.status_code}')
                failure_flag = True
        if failure_flag:
            print('There was at least one error on upload, exiting...')
            exit()
    return

def main():
    # https://www.netlify.com/blog/2020/09/24/how-to-deploy-a-simple-site-using-postman-and-the-netlify-api/
    site_name = os.getenv('NETLIFY_SITE_NAME') # lowercase, no spaces, not sure about '-'

    # Make sure this is correct EVERY TIME!
    # shasum site/<file>
    files = {
        'files':{
            'index.html': 'bb10a22a88212f5cb579c0f9b890874bbb02f85d'
        }
    }
    # TODO: Automate this? ^

    # Vars to skip steps in case of error during deployment
    site_id = os.getenv('NETLIFY_SITE_ID')
    deploy_id = os.getenv('NETLIFY_DEPLOY_ID')

    # Create a site
    if not site_id:
        site_response = init_site(site_name)
        if 'errors' in site_response:
            print('An error occured! Aborting...')
            exit()
        site_id = site_response['id']
        print(f'Site created with ID: {site_id}')
    
    # Create a deploy by sending the list of files that will be included
    if not deploy_id:
        create_deploy_ret = create_deploy(site_id, files)
        deploy_id = create_deploy_ret['id']
        print(f'Deploy created with ID: {deploy_id}')

    # Upload the files to the deploy
    upload_files(deploy_id, files)
    
    print('Deployment completed!')

if __name__ == '__main__':
    main()

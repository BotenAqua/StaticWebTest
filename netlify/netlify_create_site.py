import os
import requests
import json

netlify_api_url = 'https://api.netlify.com/api/v1'

def get_vars():
    netlify_token = os.getenv('NETLIFY_API_KEY')
    netlify_site_name = os.getenv('NETLIFY_SITE_NAME')
    
    if netlify_token is None:
        print('Missing NETLIFY_API_KEY, exiting...')
        exit()
    if netlify_site_name is None:
        print('Missing NETLIFY_SITE_NAME, exiting...')
        exit()
    return netlify_token, netlify_site_name

def init_site(netlify_token, netlify_site_name):
    headers = {
        'Authorization': f'Bearer {netlify_token}',
        'Content-Type': 'application/json'
    }

    data = {
        'name': netlify_site_name
    }
    
    response = requests.post(f'{netlify_api_url}/sites', headers=headers, data=json.dumps(data))
    print(f'Init Site - response code {response.status_code}')
    return response.json()


if __name__ == '__main__':
    netlify_token, netlify_site_name = get_vars()
    site = init_site(netlify_site_name)
    print(f'Site created with ID: {site['id']}')
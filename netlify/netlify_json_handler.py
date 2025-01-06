import os
import json

def get_files_json(file_location='', file_name='files.json'):
    file_path = os.path.join(file_location, file_name)
    with open(file_path, 'r') as file:
        # print(file.read())
        data = json.load(file)
    return data
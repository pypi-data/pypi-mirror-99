# Imports
from easysettings import EasySettings
import requests
import torch
import torch.nn as nn
import io
import json

# Functions
api_endpoint = 'http://3.101.141.59:8079'

settings = EasySettings('./.starfruit.conf')

# https://pypi.org/project/simple-settings/
# Easy way for us to store API-key?

# todo: flesh out function


def auth(apikey):
    if (isinstance(apikey, str)):
        settings.setsave('apikey', apikey)
    else:
        print('API Key must be a string.')
        return

    r = requests.post(api_endpoint + '/files',
                      json={"apikey": settings.get("apikey")})

    if r.status_code == 401:
        print('Unauthorized: Invalid API Key')
        return
    elif r.status_code == 200:
        num_models = len(r.json())
        print(f'Successfully Authenticated: {num_models} models found.')


def pt_deploy(model, name, handlerType):
    # todo: flesh out function
    # todo: add handlerType to args as well as a place to indicate customHandler (not sure how we'd do that since we need to upload a .py to the serve), customHandler would probably be
    # a kwarg?

    # Error handling: Check if model exists and is of type (nn.Module), check if name is valid string, check if handlerType is set, if custom check if customHandler is provided
    if (not isinstance(model, nn.Module)):
        print('Model must be a nn.Module.')
        return

    if settings.has_option('apikey'):
        api_key = settings.get("apikey")
    else:
        print('API Key not defined. Must call auth() before other functions.')
        return

    m = torch.jit.script(model)

    torch.jit.save(m, f'{name}.pt')

    files = {'files': open(f'{name}.pt', 'rb')}
    data = {'apikey': api_key, 'handlerType': handlerType}

    # POST request to /upload with apikey, model.pt, handlerType and customHandler if needed
    r = requests.post(api_endpoint + '/upload', files=files, data=data)

    # Maybe be fancy and show progress bar with tqdm for upload or something
    if (r.status_code == 200):
        response = r.json()
        print(response['message'] + ': ' + response['info']['model'])
        print('Timestamp: ' + response['info']['timestamp'])
    elif (r.status_code == 401):
        print('Unauthorized: Invalid API Key')
    else:
        print(f'Error: {r.status_code}')


def predict(model, timestamp, file):

    if (not isinstance(model, str)):
        print('Model name should be a string.')
        return

    if (not isinstance(timestamp, str)):
        print('Timestamp should be a string.')
        return

    if settings.has_option('apikey'):
        api_key = settings.get("apikey")
    else:
        print('API Key not defined. Must call auth() before other functions.')
        return

    files = {'file': (file, open(file, 'rb'), 'image/jpeg')}
    data = {'apikey': api_key, 'model': model, 'timestamp': timestamp}

    r = requests.post(api_endpoint + '/predict', data=data, files=files)

    if (r.status_code == 200):
        response = r.json()
        print(response)
    elif (r.status_code == 401):
        print('Unauthorized: Invalid API Key')
    else:
        print(f'Error: {r.status_code}')

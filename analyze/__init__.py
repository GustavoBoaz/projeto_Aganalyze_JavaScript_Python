import flask, os, json
from flask import Flask

def create_app():
    server = Flask(__name__, static_url_path='', instance_relative_config=True)
    server.config.from_pyfile('config.py')

    # Check if we are in a Cloud Foundry environment, i.e., on IBM Cloud
    # If we are on IBM Cloud, obtain the credentials from the environment.
    # Else, read them from file.
    # Thereafter, set up the services and module with the obtained credentials.
    if 'VCAP_SERVICES' in os.environ:
        vcapEnv=json.loads(os.environ['VCAP_SERVICES'])

        # Update Flask configuration
        server.config.update({'SERVER_NAME': json.loads(os.environ['VCAP_APPLICATION'])['uris'][0],
                            'SECRET_KEY': 'gbsouza',
                            'PREFERRED_URL_SCHEME': 'https',
                            'PERMANENT_SESSION_LIFETIME': 1800, # session time in second (30 minutes)
                            'DEBUG': False})

    else:
        server.config.update({'SERVER_NAME': '127.0.0.1:8050',
                            'SECRET_KEY': 'gbsouza',
                            'PREFERRED_URL_SCHEME': 'http',
                            'PERMANENT_SESSION_LIFETIME': 2592000, # session time in seconds (30 days)
                            'DEBUG': True})
    return server

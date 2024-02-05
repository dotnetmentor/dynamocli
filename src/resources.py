import boto3

from src.document_visualizer import DocumentVisualizer

def get_resources_from_config(config: dict):
    authentication_type = config.get('authentication', 'local')
    table_name = config.get('tablename')
    if authentication_type == 'local':
        port = config.get('port', '8000')
        client = boto3.client(
            'dynamodb', endpoint_url=f'http://localhost:{port}', region_name=config.get('region'))
        table = boto3.resource(
            'dynamodb', endpoint_url=f'http://localhost:{port}', region_name=config.get('region')).Table(table_name)
    elif (authentication_type == 'credentials'):
        session = boto3.Session(
            profile_name=config.get('profile', 'default'), region_name=config.get('region'))
        client = session.client('dynamodb')
        table = session.resource('dynamodb').Table(table_name)
    elif (authentication_type == 'env'):
        session = boto3.Session(region_name=config.get('region'))
        client = session.client('dynamodb')
        table = session.resource('dynamodb').Table(table_name)
    else:
        client = None
        table = None
    visualizer = DocumentVisualizer()
    return client, table, visualizer
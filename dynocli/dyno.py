from appdirs import user_config_dir
import os.path
from os import mkdir
import argparse
import configparser

try:
    from .dynamo_gateway import DynamoGateway
except:
    from dynamo_gateway import DynamoGateway


def update_configuration(config: configparser.ConfigParser, is_new=False):
    if (is_new):
        connection = {}
        auth = input('Select authentication type [local, credentials, env] ')
        if not auth in ['local', 'credentials', 'env']:
            raise Exception(f'Invalid authentication type: {auth}')
        connection['authentication'] = auth
        if auth == 'local':
            port = input(
                'Select which port your local dynamoDB runs on. Default: 8000 ')
            if not port:
                port = '8000'
            connection['port'] = port
        elif auth == 'credentials':
            profile = input(
                'Enter profile name as set in your .credentials file ')
            connection['profile'] = profile
        if auth in ['env', 'credentials']:
            region = input('Enter your AWS region ')
            connection['region'] = region
        table_name = input(
            'Enter name of the table on which you wish to perform operations ')
        connection['TableName'] = table_name
        config['Connection'] = connection
    else:
        name = input('Enter parameter to add/update ')
        value = input('Enter new value ')
        config['Connection'][name] = value
    return config


def read_update_values_from_input():
    updates = []
    done = False
    while not done:
        op = input('Select operation to use (Set/remove) ').lower()
        update = {}
        if (not op or op in ['s', 'set']):
            update['operation'] = 'SET'
            attr = input('Select attribute to update ')
            update['attribute'] = attr
            value = input('Enter new value ')
            update['value'] = value
        elif op in ['r', 'remove']:
            update['operation'] = 'REMOVE'
            attr = input('Select attribute to remove ')
            update['attribute'] = attr
        updates.append(update)
        resp = input('Add more operations? (y/N) ')
        done = not resp or not resp.lower().startswith('y')
    return updates

def print_config(config: configparser.ConfigParser):
    conn = config['Connection']
    for key in conn:
        print(f'{key}: {conn[key]}')

def main():
    parser = argparse.ArgumentParser(
        description="A simple command line tool to interact with a DynamoDB instance."
    )
    parser.add_argument(
        'op', choices=['describe', 'query', 'scan', 'get-config', 'set-config'])
    parser.add_argument('--verbose', '-v',
                        help='increase output verbosity', action='store_true')
    parser.add_argument(
        '--index', '-i', help='Specify name of index to use. Omit "pk"', default='')
    parser.add_argument(
        '--pk', help='The partition key value of the index to query')
    parser.add_argument('--sk', help='The sort key value. Defaults to --pk')
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config_dir_path = user_config_dir('dynocli')
    config_file_path = os.path.join(config_dir_path, '.config.ini')
    if args.op == 'set-config':
        if not os.path.isdir(config_dir_path):
            mkdir(path=config_dir_path)
        is_new = not os.path.isfile(config_file_path)
        print(config_dir_path)
        if not is_new:
            config.read(config_file_path)
        config = update_configuration(config=config, is_new=is_new)
        with open(config_file_path, 'w') as config_file:
            config.write(config_file)
        return
    if not os.path.isfile(config_file_path):
        raise Exception(
            'No configuration file found. Use --set-config to create one')
    config.read(config_file_path)
    if (args.op == 'get-config'):
        config.read(config_file_path)
        print_config(config)
    dynamo_gateway = DynamoGateway(config, args.verbose)
    if args.op == 'describe':
        dynamo_gateway.describe_table()
    elif (args.op == 'query'):
        index = args.index
        pk = args.pk
        sk = args.pk if args.sk == 'pk' else args.sk if args.sk else ''
        items = dynamo_gateway.query(index, pk, sk)
        if (items):
            resp = input("Select next action: [delete/update/Quit] ").lower()
            if (resp == 'd' or resp == 'delete'):
                i = 0
                if len(items) > 1:
                    valid_index = False
                    while (not valid_index):
                        i = int(
                            input('Select which item to delete (0-{}) '.format(len(items)-1)))
                        if (i < len(items)):
                            valid_index = True
                        else:
                            print(
                                "Incorrect index. Please enter number between 0 and {} ".format(len(items)-1))
                item = items[i]
                r = dynamo_gateway.delete_item(item.get('pk'), item.get('sk'))
                if (r.get('ResponseMetadata').get('HTTPStatusCode') == 200):
                    print("Successfully deleted item")
                else:
                    print(
                        "Something went wrong when attempting to delete item:\n {}".format(r))
            elif (resp == 'u' or resp == 'update'):
                i = 0
                if len(items) > 1:
                    valid_index = False
                    while (not valid_index):
                        i = int(
                            input('Select which item to delete (0-{}) '.format(len(items)-1)))
                        if (i < len(items)):
                            valid_index = True
                        else:
                            print(
                                "Incorrect index. Please enter number between 0 and {} ".format(len(items)-1))
                item = items[i]
                updates = read_update_values_from_input()
                dynamo_gateway.update_item(
                    item.get('pk'), item.get('sk'), updates=updates)
            elif resp == 'q' or resp == 'quit':
                print('Quitting')
        else:
            print("No items found with index {} = pk: {}, sk: {}".format(
                index, pk, sk))
    elif args.op == 'scan':
        key = input('A ')
        opr = input('opr ')
        val = input('val ')
        # limit = int(input('limit '))
        dynamo_gateway.scan(opr=opr, key=key, value=val)


if __name__ == '__main__':
    main()

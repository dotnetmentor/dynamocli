import argparse

from src.dynamo_gateway import DynamoGateway
from src.configuration import Configuration
from src.resources import get_resources_from_config


def update_configuration(config: Configuration):
      key = input('Enter parameter to add/update ')
      value = input('Enter new value ')
      config.set_value(key, value)


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
        '--pk', help='The partition key value of the index to query against.')
    parser.add_argument('--sk', help='The sort key value.')
    args = parser.parse_args()
    conf = Configuration()
    if args.op == 'set-config':
        update_configuration(conf)
        conf.save_config()
        return
    if (args.op == 'get-config'):
        conf.print_config()
        return
    config = conf.export()
    client, table, visualizer = get_resources_from_config(config)
    dynamo_gateway = DynamoGateway(client, table, visualizer, args.verbose)
    if args.op == 'describe':
        description = dynamo_gateway.describe_table()
        print(description)
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

from logging import getLogger

from boto3.dynamodb.conditions import Key, ConditionExpressionBuilder

import itertools
from operator import itemgetter


class DynamoGateway:
    def __init__(self, client, table, visualizer, verbose=False) -> None:
        log_level = 'DEBUG' if verbose else 'INFO'
        self.logger = getLogger(__name__)
        self.logger.setLevel(log_level)
        self.table = table
        self.client = client
        self.visualizer = visualizer

    def delete_item(self, pk, sk):
        table = self.table
        if table is None:
            self.logger.error('No table is configured')
            return
        if (pk is None or sk is None):
            raise Exception(
                'You need to supply both pk and sk. Got {}, {}', pk, sk)
        response = table.delete_item(
            Key={
                'pk': pk,
                'sk': sk
            },
            ReturnValues='ALL_OLD'
        )
        if (response.get('ResponseMetadata').get('HTTPStatusCode') == 200):
            self.logger.info("Successfully deleted item")
        else:
            self.logger.error(
                "Something went wrong when attempting to delete item:\n {}".format(response))
        
        print('HELLO?')
        print(response)
        return response

    def update_item(self, pk, sk, **kwargs):
        table = self.table
        if table is None:
            self.logger.error('No table is configured')
            return
        upsert = kwargs.get('upsert', False)
        table_params = {
            'Key': {
                'pk': pk,
                'sk': sk
            },
            'ReturnValues': 'ALL_NEW'
        }
        get_attr = itemgetter('operation')
        updates = kwargs.get('updates')
        grouped_updates = [list(g) for k, g in itertools.groupby(
            sorted(updates, key=get_attr), get_attr)]

        update_expression = ''
        attribute_values = {}
        for j, group in enumerate(grouped_updates):
            if not j == 0:
                update_expression += ' '
            update_expression += '{} '.format(group[0].get('operation'))
            for i, update in enumerate(group):
                attr = update.get("attribute")
                if update.get('operation') == 'SET':
                    expr = '{}=:{}'.format(attr, attr)
                    if not i == 0:
                        expr = ', ' + expr
                    update_expression += expr
                    if (value := update.get('value')):
                        attribute_values[':{}'.format(
                            attr)] = value
                else:
                    expr = f'{attr}'
                    if not i == 0:
                        expr = ', ' + expr
                    update_expression += expr

        table_params['UpdateExpression'] = update_expression
        if len(attribute_values.keys()) > 0:
            table_params['ExpressionAttributeValues'] = attribute_values
        if (not upsert):
            table_params['ConditionExpression'] = 'attribute_exists(pk)'
        self.logger.debug(table_params)
        result = table.update_item(**table_params)
        self.logger.debug(result)
        return result

    def query(self, index, value, sk, showResult=True):
        if self.table is None:
            self.logger.error('No table is configured')
            raise Exception('No table was found, check your connection config')
        resp = {}
        builder = ConditionExpressionBuilder()
        index = index if index else ''
        if (sk):
            key_expr, attribute_names, attribute_values = builder.build_expression(
                Key('{}pk'.format(index)).eq(value) & Key('{}sk'.format(index)).begins_with(sk), True)
        else:
            key_expr, attribute_names, attribute_values = builder.build_expression(
                Key('{}pk'.format(index)).eq(value), True)

        if (index):
            resp = self.table.query(
                IndexName=index,
                TableName=self.table.table_name,
                KeyConditionExpression=key_expr,
                ExpressionAttributeNames=attribute_names,
                ExpressionAttributeValues=attribute_values)
        else:
            resp = self.table.query(
                KeyConditionExpression=key_expr,
                ExpressionAttributeNames=attribute_names,
                ExpressionAttributeValues=attribute_values)

        items = resp.get('Items')
        if (showResult):
            self.visualizer.print_items(items=items)
        return items

    def scan(self, **kwargs):
        key = kwargs.get('key')
        opr = kwargs.get('opr')
        val = kwargs.get('value')
        items = []
        keyObject = Key(key)
        conditionMethod = getattr(keyObject, opr)
        filter_expression = conditionMethod(val)
        res = self.table.scan(FilterExpression=filter_expression, Limit=100)
        items.extend(res.get('Items'))

        last_evaluated = res.get('LastEvaluatedKey')
        done = last_evaluated is None
        i = 1
        while not done and i < 100:
            print('scan iteration', i)
            iteration_res = self.table.scan(
                FilterExpression=filter_expression, Limit=100, ExclusiveStartKey=last_evaluated)
            items.extend(iteration_res.get('Items'))
            last_evaluated = iteration_res.get('LastEvaluatedKey')
            done = last_evaluated is None
            i += 1

        self.visualizer.print_items(items)

    def describe_table(self):
        description = self.client.describe_table(
            TableName=self.table.table_name)
        self.logger.debug(description)
        
        return description

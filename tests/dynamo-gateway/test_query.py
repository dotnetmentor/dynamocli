from src.dynamo_gateway import DynamoGateway

def test_query_item_gets_all_items(table, client, visualizer):
    table.put_item(Item={'pk': 'test123', 'sk': 'test12'})
    table.put_item(Item={'pk': 'test123', 'sk': 'test123'})
    table.put_item(Item={'pk': 'test123', 'sk': 'test1234'})
    gateway = DynamoGateway(client, table, visualizer)
    items = gateway.query(None, 'test123', 'test', False)
    assert len(items) == 3


def test_query_item_gets_one_item(table, client, visualizer):
    table.put_item(Item={'pk': 'test123', 'sk': 'test12'})
    table.put_item(Item={'pk': 'test123', 'sk': 'test123'})
    table.put_item(Item={'pk': 'test123', 'sk': 'test1234'})
    gateway = DynamoGateway(client, table, visualizer)
    items = gateway.query(None, 'test123', 'test1234', False)
    assert len(items) == 1


def test_query_item_gets_no_items(table, client, visualizer):
    table.put_item(Item={'pk': 'test123', 'sk': 'test12'})
    table.put_item(Item={'pk': 'test123', 'sk': 'test123'})

    gateway = DynamoGateway(client, table, visualizer)
    items = gateway.query(None, 'test123', 'test1234', False)
    assert len(items) == 0


def test_query_items_by_secondary_index(table, client, visualizer):
    table.put_item(Item={'pk': 'primary', 'sk': 'primary_sort',
                   'gsi1pk': 'test123', 'gsi1sk': 'test12'})
    table.put_item(Item={'pk': 'primary', 'sk': 'primary_sort2',
                   'gsi1pk': 'test123', 'gsi1sk': 'test123'})

    gateway = DynamoGateway(client, table, visualizer)
    items = gateway.query('gsi1', 'test123', 'test', False)

    assert len(items) == 2

def test_query_items_when_no_sk(client, table, visualizer):
    table.put_item(Item={'pk': 'test123', 'sk': 'test12'})
    table.put_item(Item={'pk': 'test123', 'sk': 'test123'})

    gateway = DynamoGateway(client, table, visualizer)
    items = gateway.query(None, 'test123', None, False)
    assert len(items) == 2


def test_query_items_by_secondary_index__when_no_sk(client, table, visualizer):
    table.put_item(Item={'pk': 'test123', 'sk': 'test12', 'gsi1pk': 'secondary123', 'gsi1sk': 'secondary12'})
    table.put_item(Item={'pk': 'test123', 'sk': 'test123', 'gsi1pk': 'secondary123', 'gsi1sk': 'secondary123'})

    gateway = DynamoGateway(client, table, visualizer)
    items = gateway.query('gsi1', 'secondary123', None, False)
    assert len(items) == 2
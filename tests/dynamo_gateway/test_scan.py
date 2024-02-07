import pytest
from src.dynamo_gateway import DynamoGateway


@pytest.fixture(scope='function')
def dataset():
    items = []
    occupations = ['Developer', 'Tester', 'Designer', 'Boss', 'Media Manager',
                   'Sales Manager', 'Accountant', 'HR', 'Admin', 'Support']
    rooms = [
      {'name': 'Kitchen', 'capacity': 10},
      {'name': 'Conference Room 1', 'capacity': 8},
      {'name': 'Office 1', 'capacity': 4},
      {'name': 'Office 2', 'capacity': 4},
      {'name': 'Conference Room 2', 'capacity': 8},
      {'name': 'Lobby', 'capacity': 20},
      {'name': 'Storage Room', 'capacity': 2},
      {'name': 'Server Room', 'capacity': 6},
      {'name': 'Reception', 'capacity': 10},
      {'name': 'Meeting Room', 'capacity': 8}
    ]
    for i in range(100):
        items.append({'pk': 'test#employee', 'sk': f'test#employee#{i}',
                     'occupation': occupations[i % len(occupations)]})
    for i in range(100):
        items.append({'pk': 'test#room', 'sk': f'test#room#{i}',
                     'room': rooms[i % len(rooms)].get('name'), 'capacity': rooms[i % len(rooms)].get('capacity')})
    return items

def test_scan_table_returns_correct_items(table, client, visualizer):
    table.put_item(Item={'pk': 'test123', 'sk': 'test123',
                   'occupation': 'Developer'})
    table.put_item(
        Item={'pk': 'test123', 'sk': 'test1234', 'occupation': 'Tester'})
    table.put_item(
        Item={'pk': 'test123', 'sk': 'test12345', 'occupation': 'Tester'})
    gateway = DynamoGateway(client, table, visualizer)
    kwargs = {'opr': 'eq', 'value': 'Developer', 'key': 'occupation'}
    items = gateway.scan(**kwargs)
    assert len(items) == 1
    visualizer.print_items.assert_called_once()

def test_scan_table_returns_correct_items_with_serveral_iterations(table, client, visualizer, dataset):
    for item in dataset:
        table.put_item(Item=item)
    gateway = DynamoGateway(client, table, visualizer)
    kwargs = {'opr': 'begins_with', 'value': 'Dev', 'key': 'occupation'}
    items = gateway.scan(**kwargs)
    assert len(items) == 10

    kwargs = {'opr': 'begins_with', 'value': 'Office', 'key': 'room'}
    items = gateway.scan(**kwargs)
    assert len(items) == 20
    visualizer.print_items.call_count == 2

def test_scan_table_returns_items_with_greater_capacity(table, client, visualizer, dataset):
    for item in dataset:
        table.put_item(Item=item)
    gateway = DynamoGateway(client, table, visualizer)
    kwargs = {'opr': 'gt', 'value': 8, 'key': 'capacity'}
    items = gateway.scan(**kwargs)
    assert len(items) == 30
    visualizer.print_items.assert_called_once()

def test_scan_table_returns_items_with_less_capacity(table, client, visualizer, dataset):
    for item in dataset:
        table.put_item(Item=item)
    gateway = DynamoGateway(client, table, visualizer)
    kwargs = {'opr': 'lt', 'value': 5, 'key': 'capacity'}
    items = gateway.scan(**kwargs)
    assert len(items) == 30
    visualizer.print_items.assert_called_once()

def test_scan_table_returns_items_with_less_than_or_equal_capacity(table, client, visualizer, dataset):
    for item in dataset:
        table.put_item(Item=item)
    gateway = DynamoGateway(client, table, visualizer)
    kwargs = {'opr': 'lte', 'value': 6, 'key': 'capacity'}
    items = gateway.scan(**kwargs)
    assert len(items) == 40
    visualizer.print_items.assert_called_once()

def test_scan_table_returns_items_with_greater_than_or_equal_capacity(table, client, visualizer, dataset):
    for item in dataset:
        table.put_item(Item=item)
    gateway = DynamoGateway(client, table, visualizer)
    kwargs = {'opr': 'gte', 'value': 8, 'key': 'capacity'}
    items = gateway.scan(**kwargs)
    assert len(items) == 60
    visualizer.print_items.assert_called_once()

# def test_scan_table_returns_items_with_capacity_between_5_and_10(table, client, visualizer, dataset):
#     for item in dataset:
#         table.put_item(Item=item)
#     gateway = DynamoGateway(client, table, visualizer)
#     kwargs = {'opr': 'between', 'value': [5, 10], 'key': 'capacity'}
#     items = gateway.scan(**kwargs)
#     assert len(items) == 30

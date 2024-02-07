import pytest
from src.dynamo_gateway import DynamoGateway

def test_update_item_change_value(table, client, visualizer):
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk,'sk': sk, 'occupation': 'Integration Tester'})
  gateway = DynamoGateway(client, table, visualizer)
  updates = {'operation': 'SET', 'attribute': 'occupation', 'value': 'Unit Tester'}
  response = gateway.update_item(pk, sk, updates=[updates])
  assert response is not None
  assert response.get('Attributes').get('occupation') == 'Unit Tester'
  
def test_update_item_remove_attributes(table, client, visualizer):
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk,'sk': sk, 'occupation': 'Integration Tester', 'rate': 'hourly', 'tech_savvy': False})
  gateway = DynamoGateway(client, table, visualizer)
  updates = [{'operation': 'REMOVE', 'attribute': 'rate'}, { 'operation': 'REMOVE', 'attribute': 'tech_savvy'}]
  response = gateway.update_item(pk, sk, updates=updates)
  assert response is not None
  assert response.get('Attributes').get('rate') is None
  assert response.get('Attributes').get('tech_savvy') is None

def test_update_item_change_integer_value(table, client, visualizer):
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk,'sk': sk, 'age': 25})
  gateway = DynamoGateway(client, table, visualizer)
  updates = {'operation': 'SET', 'attribute': 'age', 'value': 30}
  response = gateway.update_item(pk, sk, updates=[updates])
  assert response is not None
  assert response.get('Attributes').get('age') == 30

def test_update_item_several_operations(table, client, visualizer):
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk,'sk': sk, 'age': 25, 'occupation': 'Developer'})
  gateway = DynamoGateway(client, table, visualizer)
  updates = [{'operation': 'SET', 'attribute': 'age', 'value': 30}, {'operation': 'REMOVE', 'attribute': 'occupation'}]
  response = gateway.update_item(pk, sk, updates=updates)
  assert response is not None
  assert response.get('Attributes').get('age') == 30
  assert response.get('Attributes').get('occupation') is None

def test_update_item_add_new_attributes(table, client, visualizer):
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk,'sk': sk, 'age': 25})
  gateway = DynamoGateway(client, table, visualizer)
  updates = [{'operation': 'SET', 'attribute': 'occupation', 'value': 'Developer'}, { 'operation': 'SET', 'attribute': 'salary', 'value': 30000}]
  response = gateway.update_item(pk, sk, updates=updates)
  assert response is not None
  assert response.get('Attributes').get('occupation') == 'Developer'
  assert response.get('Attributes').get('salary') == 30000
  assert response.get('Attributes').get('age') == 25

def test_update_item_table_is_none(client, table, visualizer):
  gateway = DynamoGateway(client, None, visualizer)
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk, 'sk': sk, 'occupation': 'Developer'})
  with pytest.raises(ValueError, match='No table was found, check your connection config'):
    gateway.update_item(pk, sk, updates=[{'operation': 'SET', 'attribute': 'age', 'value': 30}])
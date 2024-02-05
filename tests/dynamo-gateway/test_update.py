from src.dynamo_gateway import DynamoGateway

def test_update_item(table, client, visualizer):
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk,'sk': sk, 'occupation': 'Integration Tester'})
  gateway = DynamoGateway(client, table, visualizer)
  updates = {'operation': 'SET', 'attribute': 'occupation', 'value': 'Unit Tester'}
  response = gateway.update_item(pk, sk, updates=[updates])
  assert response is not None
  assert response.get('Attributes').get('occupation') == 'Unit Tester'
  
  
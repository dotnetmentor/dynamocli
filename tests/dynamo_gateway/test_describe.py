from src.dynamo_gateway import DynamoGateway

def test_describe_table(client, table, visualizer):
  gateway = DynamoGateway(client, table, visualizer)
  description = gateway.get_table_description()
  assert description is not None
  table = description.get('Table') 
  assert table.get('TableName') == 'test_table'
  assert table.get('TableStatus') == 'ACTIVE'
  attribute_definitions = table.get('AttributeDefinitions')
  names = [d['AttributeName'] for d in attribute_definitions]
  assert len(attribute_definitions) == 4
  assert names == ['pk', 'sk', 'gsi1pk', 'gsi1sk']

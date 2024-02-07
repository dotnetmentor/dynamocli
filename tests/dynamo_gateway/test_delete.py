import pytest
from src.dynamo_gateway import DynamoGateway


def test_delete_item(client, table, visualizer):
    pk_to_remove = 'test123'
    sk_to_remove = 'test123'
    table.put_item(Item={'pk': pk_to_remove, 'sk': sk_to_remove})
    table.put_item(Item={'pk': 'test123', 'sk': 'test1234'})
    
    gateway = DynamoGateway(client, table, visualizer)
    response = gateway.delete_item(pk_to_remove, sk_to_remove)
    assert response is not None
    
    attributes = response.get('Attributes')
    assert attributes.get('pk') == pk_to_remove
    assert attributes.get('sk') == sk_to_remove

    remaining_items = table.scan()
    assert remaining_items.get('Count') == 1

  
def test_delete_item_when_table_is_none(client, table, visualizer):
  gateway = DynamoGateway(client, None, visualizer)
  pk = 'test123'
  sk = 'test123'
  table.put_item(Item={'pk': pk, 'sk': sk})  
  with pytest.raises(ValueError, match='No table was found, check your connection config'):
    gateway.delete_item(pk, sk)

def test_delete_item_when_pk_is_none(client, table, visualizer):
  gateway = DynamoGateway(client, table, visualizer)
  sk = 'test123'
  with pytest.raises(ValueError, match='You need to supply both pk and sk. Got None, test123'):
    gateway.delete_item(None, sk)

    

from src.dynamo_gateway import DynamoGateway


def test_delete_item(table, client, visualizer):
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
    
    

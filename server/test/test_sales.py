def test_get_sales(client):
    response = client.get('/sales')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    data = response.json()
    assert type(data) is dict
    assert 'data' in data
    assert type(data['data']) is list

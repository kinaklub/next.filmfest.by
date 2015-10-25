def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200


def test_nothing():
    pass

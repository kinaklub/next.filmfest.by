import pytest


@pytest.mark.django_db
def test_locale_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response['Location'] == 'http://testserver/en/'


@pytest.mark.django_db
def test_homepage(client):
    response = client.get('/en/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_resultspage_2012(client):
    response = client.get('/en/results2012/')
    assert response.status_code == 200
    assert '2012: how it was' in response.content
    assert 'Agricola de Cologne' in response.content


@pytest.mark.django_db
def test_resultspage_2013(client):
    response = client.get('/en/results2013/')
    assert response.status_code == 200
    assert '2013: good memories' in response.content
    assert 'Volha Dashuk' in response.content

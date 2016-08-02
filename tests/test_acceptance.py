import pytest


@pytest.mark.django_db
def test_locale_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response['Location'] == '/en/'


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


@pytest.mark.django_db
def test_pages(client):
    # given web client and home page added by migrations

    # when image with title 'Cory McAbee' is requested via public API
    response = client.get('/api/v2/pages/', {'slug': 'home'})
    data = response.json()

    # response contains one image with the corresponding title
    assert response.status_code == 200
    assert data['meta']['total_count'] == 1
    assert data['items'][0]['title'] == 'Homepage'


@pytest.mark.django_db
def test_images(client):
    # given web client and Cory McAbee image uploaded by migrations
    cory_mcabee = 'Cory McAbee'

    # when image with title 'Cory McAbee' is requested via public API
    response = client.get('/api/v2/images/', {'title': cory_mcabee})
    data = response.json()

    # response contains one image with the corresponding title
    assert response.status_code == 200
    assert data['meta']['total_count'] == 1
    assert data['items'][0]['title'] == cory_mcabee

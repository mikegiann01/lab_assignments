import pytest
from flask import url_for, json
from app import app as flask_app

@pytest.fixture
def app():
    app = flask_app
    app.config.update({
        "TESTING": True,
    })
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    with client.application.app_context():
        response = client.get(url_for('index'))
    assert response.status_code == 200
    assert 'text/html' in response.content_type
    assert 'Lebron James' in response.get_data(as_text=True)

def test_create_player(client):
    response = client.post(url_for('create_player'), data={
        'name': 'Stephen Curry',
        'position': 'Guard',
        'team': 'Golden State Warriors'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Stephen Curry' in response.get_data(as_text=True)

def test_get_players(client):
    response = client.get(url_for('get_players'))
    assert response.status_code == 202
    data = response.get_json()
    assert 'players' in data
    assert len(data['players']) >= 1  

def test_update_player(client):
    response = client.put(url_for('update_player', index=0), data={
        'name': 'Kobe Bryant',
        'position': 'Guard',
        'team': 'Los Angeles Lakers'
    })
    assert response.status_code == 200
    assert 'Kobe Bryant' in response.get_data(as_text=True)

def test_delete_player(client):

    response = client.delete(url_for('delete_player', index=0))
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['players']) == 1 

if __name__ == "__main__":
    pytest.main()
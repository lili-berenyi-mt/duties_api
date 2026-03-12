from backend.app import create_app
from backend.models import db
from backend.models import User
import pytest

@pytest.fixture
def client():
    app = create_app(config_name="testing")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all() 

@pytest.fixture
def seed_user(client):
    with client.application.app_context():
        user = User(username="user", role="user")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user) 
    return user

def test_api_verify_login_success(client, seed_user):
    response = client.post('/verify-login', json={
        'username': 'user',
        'password': 'password'
    })

    assert response.status_code == 200

def test_login_fails_with_invalid_username(client, seed_user):
    response = client.post('/verify-login', json={
        'username': 'non_existent_user',
        'password': 'any_password'
    })
    
    assert response.status_code == 401
    assert response.json['error'] == "Invalid username or password"

def test_login_fails_with_wrong_password(client, seed_user):
    response = client.post('/verify-login', json={
        'username': 'user',
        'password': 'wrong_password'
    })

    assert response.status_code == 401
    assert response.json['error'] == "Invalid username or password"
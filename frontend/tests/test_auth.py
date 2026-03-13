from frontend.app import app as frontend
import pytest

@pytest.fixture
def client():
    frontend.config['TESTING'] = True
    frontend.config['SECRET_KEY'] = 'test-secret'
    with frontend.test_client() as client:
        yield client

def test_frontend_login_sets_session_on_backend_success(client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "role": "user", "username": "user"}

    mocker.patch('requests.post', return_value=mock_response)

    client.post('/login', data={'username': 'user', 'password': 'password'})

    with client.session_transaction() as session:
        assert session['id'] == 1
        assert session['role'] == 'user'

def test_login_shows_error_message_on_wrong_credentials(client, mocker):
    mock_resp = mocker.Mock()
    mock_resp.status_code = 401
    mocker.patch('requests.post', return_value=mock_resp)

    response = client.post('/login', data={
        'username': 'wrong_user',
        'password': 'wrong_password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_admin_features_hidden_from_non_admin(client):
    response = client.get('/')
    assert b"Add Duty" not in response.data
    assert b"Delete" not in response.data
from frontend.app import app as frontend
import pytest

@pytest.fixture
def client():
    frontend.config['TESTING'] = True
    frontend.config['SECRET_KEY'] = 'test-secret'
    with frontend.test_client() as client:
        yield client

def test_get_logs_unauthenticated_fails(client):
    response = client.get('/logs')
    assert response.status_code == 403

def test_get_logs_non_admin_fails(client):
    with client.session_transaction() as session:
        session['role'] = 'user'

    response = client.get('/logs')
    
    assert response.status_code == 403

def test_frontend_renders_logs_for_admin(client, mocker):
    with client.session_transaction() as session:
        session['role'] = 'admin'

    mock_data = [
        {"timestamp": "2026-03-13 14:00", "method": "GET", "path": "/duties", "status_code": 200},
        {"timestamp": "2026-03-13 14:05", "method": "POST", "path": "/duties", "status_code": 429}
    ]
    
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data
    mocker.patch('requests.get', return_value=mock_response)

    response = client.get('/logs')

    assert response.status_code == 200
    assert b"Logs" in response.data
    assert b"429" in response.data 
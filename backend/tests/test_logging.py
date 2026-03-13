from backend.app import create_app
from backend.models import db, RequestLog
import pytest

@pytest.fixture
def client():
    app = create_app(config_name="testing")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all() 

def test_logging_on_request(client):
    client.get('/duties')

    latest_log = RequestLog.query.first()

    assert latest_log is not None
    assert latest_log.path == '/duties'
    assert latest_log.method == 'GET'
    assert latest_log.status_code == 200

def test_logging_captures_429_errors(client):
    for _ in range(11):
        response = client.get('/duties')

    assert response.status_code == 429

    error_log = RequestLog.query.filter_by(status_code=429).first()
    assert error_log is not None
    assert error_log.path == '/duties'
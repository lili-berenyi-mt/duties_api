from backend.app import create_app
from backend.models import db, RequestLog
import pytest
import datetime

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

def test_log_query_limit_and_order(client):
    base_time = datetime.datetime.now(datetime.UTC)
    for i in range(110):
        log = RequestLog(method="GET", path=f"/path-{i}", status_code=200, timestamp=base_time + datetime.timedelta(seconds=i))
        db.session.add(log)
    db.session.commit()

    response = client.get('/logs')
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 100
    assert data[0]['path'] == "/path-109"
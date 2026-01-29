from app import create_app
from models import db
import pytest 

@pytest.fixture
def client():
    app = create_app(config_name="testing")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all() 

def test_get_duties_returns_200(client):
    result = client.get('/duties')
    assert result.status_code == 200


def test_get_duties_returns_empty_list(client):
    result = client.get('/duties')
    assert result.get_json() == []

def test_can_create_new_duty(client):
    duty = {"name": "Duty 1", "description": "Test description"}
    response = client.post('/duties', json=duty)
    assert response.status_code == 201
    result = response.get_json()
    assert result["name"] == "Duty 1"
    assert result["description"] == "Test description"

def test_created_duty_has_unique_string_id(client):
    duty = {"name": "Duty 1", "description": "Test description"}
    response = client.post('/duties', json=duty)
    result = response.get_json()
    assert "id" in result
    assert len(result["id"]) == 36

def test_creating_two_duties_results_in_unique_ids(client):
    duty1 = {"name": "Duty 1", "description": "Test description 1"}
    duty2 = {"name": "Duty 2", "description": "Test description 2"}
    response1 = client.post('/duties', json=duty1)
    response2 = client.post('/duties', json=duty2)
    assert response1.get_json()["id"] != response2.get_json()["id"]

def test_can_get_created_duty(client):
    duty = {"name": "Duty 1", "description": "Test description"}
    client.post('/duties', json=duty)
    response = client.get("/duties")
    result = response.get_json()
    assert len(result) == 1
    assert result[0]["name"] == "Duty 1"

def test_creating_duty_with_missing_name_returns_400(client):
    duty = {"description": "Test description"}
    reponse = client.post("/duties", json=duty)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields. Request must contain name and description."

def test_creating_duty_with_invalid_name_returns_400(client):
    duty_data = {"name": "test", "description": "description"}
    reponse = client.post("/duties", json=duty_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == f"Invalid name '{"test"}'. Must start with 'Duty ' followed by 1 or 2 digits (e.g., 'Duty 1')."

def test_creating_duty_with_missing_description_returns_400(client):
    duty_data = {"name": "Duty 1"}
    reponse = client.post("/duties", json=duty_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields. Request must contain name and description."

def test_creating_duty_with_invalid_description_returns_400(client):
    duty_data = {"name": "Duty 1", "description": ""}
    reponse = client.post("/duties", json=duty_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Description must be a non-empty string under 255 characters."

def test_creating_duty_with_existing_code_returns_400(client):
    duty_data = {"name": "Duty 1", "description": "Test description"}
    client.post("/duties", json=duty_data)
    reponse = client.post("/duties", json=duty_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "A duty with this name already exists."
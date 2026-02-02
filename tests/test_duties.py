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
    duty = {"code": "D1", "description": "Test description"}
    response = client.post('/duties', json=duty)
    assert response.status_code == 201
    result = response.get_json()
    assert result["code"] == "D1"
    assert result["description"] == "Test description"

def test_created_duty_has_unique_string_id(client):
    duty = {"code": "D1", "description": "Test description"}
    response = client.post('/duties', json=duty)
    result = response.get_json()
    assert "id" in result
    assert len(result["id"]) == 36

def test_creating_two_duties_results_in_unique_ids(client):
    duty1 = {"code": "D1", "description": "Test description 1"}
    duty2 = {"code": "D2", "description": "Test description 2"}
    response1 = client.post('/duties', json=duty1)
    response2 = client.post('/duties', json=duty2)
    assert response1.get_json()["id"] != response2.get_json()["id"]

def test_can_get_created_duty(client):
    duty = {"code": "D1", "description": "Test description"}
    client.post('/duties', json=duty)
    response = client.get("/duties")
    result = response.get_json()
    assert len(result) == 1
    assert result[0]["code"] == "D1"

def test_creating_duty_with_missing_code_returns_400(client):
    duty = {"description": "Test description"}
    response = client.post("/duties", json=duty)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "code" in data["error"]

def test_creating_duty_with_invalid_code_returns_400(client):
    duty_data = {"code": "Duty 1", "description": "description"}
    response = client.post("/duties", json=duty_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid code 'Duty 1'. Must start with 'D' followed by 1 or 2 digits (e.g., 'D1')."

def test_creating_duty_with_missing_description_returns_400(client):
    duty = {"code": "D1"}
    response = client.post("/duties", json=duty)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields. Request must contain code and description."

def test_creating_duty_with_invalid_description_returns_400(client):
    duty_data = {"code": "D1", "description": ""}
    reponse = client.post("/duties", json=duty_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Description must be a non-empty string under 255 characters."


def test_creating_duty_with_existing_code_returns_400(client):
    duty_data = {"code": "D1", "description": "Test description"}
    client.post("/duties", json=duty_data)
    response = client.post("/duties", json=duty_data)
    data = response.get_json()
    assert response.status_code == 400
    assert "error" in data
    assert data["error"] == "A duty with this code already exists."

def test_can_get_duty_by_id(client):
    duty_data = {"code": "D1", "description": "Test description"}
    post_response = client.post('/duties', json=duty_data)
    duty = post_response.get_json()
    duty_id = duty["id"]
    response = client.get(f"/duties/{duty_id}")
    result = response.get_json()
    assert result["id"] == duty_id
    assert result["code"] == "D1"

def test_getting_duty_with_invalid_id_returns_404(client):
    response = client.get("/duties/1234567890")
    assert response.status_code == 404

def test_deleting_existing_duty_returns_204(client):
    duty_data = {"code": "D1", "description": "Test description"}
    duty = client.post("/duties", json=duty_data).get_json()
    duty_id = duty["id"]
    response = client.delete(f"/duties/{duty_id}")
    assert response.status_code == 204

def test_deleted_duty_should_not_exitst(client):
    duty_data = {"code": "D1", "description": "Test description"}
    duty = client.post("/duties", json=duty_data).get_json()
    id = duty["id"]
    client.delete(f"/duties/{id}")
    response = client.get(f"/duties/{id}") 
    assert response.status_code == 404

def test_creating_duty_with_ksbs_returns_201(client):
    ksb_data = {"code": "K1", "description": "Ksb test description"}
    ksb_id = client.post("/ksbs", json=ksb_data).get_json()["id"]

    duty_data = {"code": "D1", "description": "Duty test description", "ksb_ids": [ksb_id]}
    response = client.post("/duties", json=duty_data)
    assert response.status_code == 201
    data = response.get_json()
    assert "K1" in data["ksbs"]

def test_creating_duty_with_invalid_ksb_returns_400(client):
    duty_data = {"code": "D1", "description": "Test description", "ksb_ids": ["123456789"]}
    response = client.post("/duties", json=duty_data)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "KSB with ID '123456789' not found"

def test_can_create_duty_with_multiple_ksbs(client):
    ksb1 = client.post("/ksbs", json={"code": "K1", "description": "Test description 1"}).get_json()
    ksb2 = client.post("/ksbs", json={"code": "S1", "description": "Test description 2"}).get_json()
    duty_data = {
        "code": "D1",
        "description": "Test description",
        "ksb_ids": [ksb1["id"], ksb2["id"]]
    }
    response = client.post("/duties", json=duty_data)

    assert response.status_code == 201
    data = response.get_json()
    assert "K1" in data["ksbs"]
    assert "S1" in data["ksbs"]
    assert len(data["ksbs"]) == 2    

def test_creating_duty_with_invalid_ksb_data_returns_400(client):
    duty_data = {
        "code": "D1",
        "description": "Multi-tasking duty",
        "ksb_ids": 0
    }
    response = client.post("/duties", json=duty_data)
    assert response.status_code == 400 
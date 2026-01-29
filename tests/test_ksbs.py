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

def test_get_ksbs_returns_200(client):
    result = client.get('/ksbs')
    assert result.status_code == 200

def test_get_ksbs_returns_empty_list(client):
    result = client.get('/ksbs')
    assert result.get_json() == []

def test_can_create_new_ksb(client):
    ksb = {"code": "K1", "description": "test description"}
    response = client.post('/ksbs', json=ksb)
    assert response.status_code == 201
    result = response.get_json()
    assert result["code"] == "K1"
    assert result["description"] == "test description"

def test_created_ksb_has_unique_string_id(client):
    ksb = {"code": "K1", "description": "test description"}
    response = client.post('/ksbs', json=ksb)
    result = response.get_json()
    assert "id" in result
    assert len(result["id"]) == 36

def test_creating_two_ksbs_results_in_unique_ids(client):
    ksb1 = {"code": "K1", "description": "test description 1"}
    ksb2 = {"code": "K2", "description": "test description 2"}
    response1 = client.post('/ksbs', json=ksb1)
    response2 = client.post('/ksbs', json=ksb2)
    assert response1.get_json()["id"] != response2.get_json()["id"]

def test_can_get_created_ksb(client):
    ksb = {"code": "K1", "description": "test description"}
    client.post('/ksbs', json=ksb)
    response = client.get("/ksbs")
    result = response.get_json()
    assert len(result) == 1
    assert result[0]["code"] == "K1"

def test_can_get_ksb_by_id(client):
    ksb_data = {"code": "K1", "description": "test description"}
    post_response = client.post('/ksbs', json=ksb_data)
    ksb = post_response.get_json()
    id = ksb["id"]
    response = client.get(f"/ksbs/{id}")
    result = response.get_json()
    assert result["id"] == id
    assert result ["code"] == "K1"

def test_getting_ksb_with_invalid_id_returns_404(client):
    response = client.get("/ksbs/1234567890")
    assert response.status_code == 404

def test_deleting_existing_ksb_returns_204(client):
    ksb_data = {"code": "K1", "description": "test description"}
    ksb = client.post("/ksbs", json=ksb_data).get_json()
    id = ksb["id"]
    response = client.delete(f"ksbs/{id}")
    assert response.status_code == 204

def test_deleted_ksb_should_not_exitst(client):
    ksb_data = {"code": "K1", "description": "test description"}
    ksb = client.post("/ksbs", json=ksb_data).get_json()
    id = ksb["id"]
    client.delete(f"/ksbs/{id}")
    response = client.get(f"/ksbs/{id}") 
    assert response.status_code == 404

def test_updated_ksb_has_updated_data(client):
    ksb_data = {"code": "K1", "description": "test description"}
    ksb = client.post("/ksbs", json=ksb_data).get_json()
    id = ksb["id"]
    updated_ksb_data = {"code": "K1", "description": "test description 2"}
    response = client.put(f"/ksbs/{id}", json=updated_ksb_data)
    assert response.status_code == 200
    updated_ksb = response.get_json()
    assert updated_ksb["code"] == "K1"
    assert updated_ksb["description"] == "test description 2"

def test_getting_ksb_after_updating_has_updated_data(client):
    ksb_data = {"code": "K1", "description": "test description"}
    ksb = client.post("/ksbs", json=ksb_data).get_json()
    id = ksb["id"]
    updated_ksb_data = {"code": "K1", "description": "test description 2"}
    client.put(f"/ksbs/{id}", json=updated_ksb_data)
    response = client.get(f"/ksbs/{id}")
    updated_ksb = response.get_json()
    assert updated_ksb["code"] == "K1"
    assert updated_ksb["description"] == "test description 2"

def test_cannot_updated_invalid_ksb(client):
    updated_ksb_data = {"code": "K1", "description": "test description 2"}
    response = client.put("/ksbs/1234567890", json=updated_ksb_data)
    assert response.status_code == 404

def test_creating_ksb_with_missing_code_returns_400(client):
    ksb_data = {"description": ""}
    reponse = client.post("/ksbs", json=ksb_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields. Request must contain code and description."

def test_creating_ksb_with_invalid_code_returns_400(client):
    ksb_data = {"code": "test", "description": "description"}
    reponse = client.post("/ksbs", json=ksb_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == f"Invalid code '{"test"}'. Must start with K, S, or B followed by 1 or 3 digits (e.g., K1, S101)."

def test_creating_ksb_with_missing_description_returns_400(client):
    ksb_data = {"code": "K1"}
    reponse = client.post("/ksbs", json=ksb_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields. Request must contain code and description."

def test_creating_ksb_with_invalid_description_returns_400(client):
    ksb_data = {"code": "K1", "description": ""}
    reponse = client.post("/ksbs", json=ksb_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Description must be a non-empty string under 255 characters."

def test_creating_ksb_with_existing_code_returns_400(client):
    ksb_data = {"code": "K1", "description": "Test description"}
    client.post("/ksbs", json=ksb_data)
    reponse = client.post("/ksbs", json=ksb_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "A KSB with this code already exists."
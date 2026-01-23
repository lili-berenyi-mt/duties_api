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
    ksb = {"code": "test code", "description": "test description"}
    response = client.post('/ksbs', json=ksb)
    assert response.status_code == 201
    result = response.get_json()
    assert result["code"] == "test code"
    assert result["description"] == "test description"

def test_created_ksb_has_unique_string_id(client):
    ksb = {"code": "test code", "description": "test description"}
    response = client.post('/ksbs', json=ksb)
    result = response.get_json()
    assert "id" in result
    assert len(result["id"]) == 36

def test_creating_two_ksbs_results_in_unique_ids(client):
    ksb1 = {"code": "test code", "description": "test description 1"}
    ksb2 = {"code": "k2", "description": "test description 2"}
    response1 = client.post('/ksbs', json=ksb1)
    response2 = client.post('/ksbs', json=ksb2)
    assert response1.get_json()["id"] != response2.get_json()["id"]

def test_can_get_created_ksb(client):
    ksb = {"code": "test code", "description": "test description"}
    client.post('/ksbs', json=ksb)
    response = client.get("/ksbs")
    result = response.get_json()
    assert len(result) == 1
    assert result[0]["code"] == "test code"

def test_can_get_ksb_by_id(client):
    ksb_data = {"code": "test code", "description": "test description"}
    post_response = client.post('/ksbs', json=ksb_data)
    ksb = post_response.get_json()
    id = ksb["id"]
    response = client.post(f"/ksbs/{id}")
    result = response.get_json()
    assert result["id"] == id
    assert result ["code"] == "test code"

def test_getting_ksb_with_invalid_id_returns_404(client):
    response = client.post("/ksbs/1234567890")
    assert response.status_code == 404

def test_deleting_existing_ksb_returns_204(client):
    ksb_data = {"code": "test code", "description": "test description"}
    ksb = client.post("/ksbs", json=ksb_data).get_json()
    id = ksb["id"]
    response = client.delete(f"ksbs/{id}")
    assert response.status_code == 204

def test_deleted_ksb_should_not_exitst(client):
    ksb_data = {"code": "test code", "description": "test description"}
    ksb = client.post("/ksbs", json=ksb_data).get_json()
    id = ksb["id"]
    client.delete(f"/ksbs/{id}")
    response = client.post(f"/ksbs/{id}") 
    assert response.status_code == 404

    

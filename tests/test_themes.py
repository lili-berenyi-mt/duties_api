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

def test_get_themes_returns_200(client):
    result = client.get('/themes')
    assert result.status_code == 200

def test_get_themes_returns_empty_list(client):
    result = client.get('/themes')
    assert result.get_json() == []

def test_can_create_new_theme(client):
    theme = {"name": "Theme 1", "description": "Test description"}
    response = client.post('/themes', json=theme)
    assert response.status_code == 201
    result = response.get_json()
    assert result["name"] == "Theme 1"
    assert result["description"] == "Test description"

def test_created_theme_has_unique_string_id(client):
    theme = {"name": "Theme 1", "description": "Test description"}
    response = client.post('/themes', json=theme)
    result = response.get_json()
    assert "id" in result
    assert len(result["id"]) == 36

def test_creating_two_themes_results_in_unique_ids(client):
    theme1 = {"name": "Theme 1", "description": "Test description 1"}
    theme2 = {"name": "Theme 2", "description": "Test description 2"}
    response1 = client.post('/themes', json=theme1)
    response2 = client.post('/themes', json=theme2)
    assert response1.get_json()["id"] != response2.get_json()["id"]

def test_can_get_created_theme(client):
    theme = {"name": "Theme 1", "description": "Test description"}
    client.post('/themes', json=theme)
    response = client.get("/themes")
    result = response.get_json()
    assert len(result) == 1
    assert result[0]["name"] == "Theme 1"

def test_can_get_theme_by_id(client):
    theme = {"name": "Theme 1", "description": "Test description"}
    post_response = client.post('/themes', json=theme)
    theme = post_response.get_json()
    id = theme["id"]
    response = client.get(f"/themes/{id}")
    result = response.get_json()
    assert result["id"] == id
    assert result ["name"] == "Theme 1"

def test_getting_theme_with_invalid_id_returns_404(client):
    response = client.get("/themes/1234567890")
    assert response.status_code == 404

def test_creating_theme_with_missing_code_returns_400(client):
    theme_data = {"description": "Test description"}
    reponse = client.post("/themes", json=theme_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields. Request must contain name and description."

def test_creating_theme_with_missing_description_returns_400(client):
    theme_data = {"name": "Theme 1"}
    reponse = client.post("/themes", json=theme_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Missing required fields. Request must contain name and description."

def test_creating_theme_with_existing_code_returns_400(client):
    theme_data = {"name": "Theme 1", "description": "Test description"}
    client.post("/themes", json=theme_data)
    reponse = client.post("/themes", json=theme_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "A theme with this name already exists."

def test_creating_theme_with_invalid_name_returns_400(client):
    theme_data = {"name": "", "description": "Test description"}
    reponse = client.post("/themes", json=theme_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Name must be a non-empty string under 255 characters."

def test_creating_theme_with_invalid_description_returns_400(client):
    theme_data = {"name": "Theme 1", "description": ""}
    reponse = client.post("/themes", json=theme_data)
    assert reponse.status_code == 400
    data = reponse.get_json()
    assert "error" in data
    assert data["error"] == "Description must be a non-empty string under 255 characters."
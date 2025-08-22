from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_imports():
    """Test that the app imports and starts successfully."""
    assert app is not None

import pytest
import json
from app import app

class TestFlaskApp:
    
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_health_check(self, client):
        """Test del endpoint de salud"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert data['service'] == 'flask-comments-api'
    def test_get_comments_empty(self, client):
        """Test obtener comentarios cuando está vacío"""
        response = client.get('/comments')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['total'] == 0
        assert data['comments'] == []
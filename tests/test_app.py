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
    def test_create_comment(self, client):
        """Test crear comentario"""
        comment_data = {
            'content': 'Este es un comentario de prueba',
            'author': 'Usuario Test'
        }
        
        response = client.post('/comments', 
                             data=json.dumps(comment_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['content'] == comment_data['content']
        assert data['author'] == comment_data['author']
        assert 'id' in data
        assert 'timestamp' in data
    
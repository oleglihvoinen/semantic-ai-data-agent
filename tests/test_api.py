from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get('/health').json() == {'status': 'ok'}

def test_unknown_metric():
    assert client.get('/api/v1/metrics/not_real').status_code == 404

def test_dimension_governance():
    response = client.post('/api/v1/query-plan', json={'metric_id': 'net_revenue', 'dimensions': ['secret_field']})
    assert response.status_code == 400

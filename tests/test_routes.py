"""Unit tests for Flask application routes."""
import pytest


@pytest.mark.unit
def test_index_requires_authentication(client):
    """Test that index page requires authentication."""
    response = client.get('/')
    
    # Should redirect to login
    assert response.status_code == 302
    assert '/login' in response.location


@pytest.mark.unit
def test_index_authenticated(auth_client):
    """Test that authenticated users can access index."""
    response = auth_client.get('/')
    
    assert response.status_code == 200
    assert b'testuser' in response.data or b'Web SSH Terminal' in response.data


@pytest.mark.unit
def test_login_page_loads(client):
    """Test that login page loads."""
    response = client.get('/login')
    
    assert response.status_code == 200
    assert b'login' in response.data.lower()


@pytest.mark.unit
def test_register_page_loads(client):
    """Test that register page loads."""
    response = client.get('/register')
    
    assert response.status_code == 200
    assert b'register' in response.data.lower()


@pytest.mark.unit
def test_change_password_requires_authentication(client):
    """Test that change password requires authentication."""
    response = client.get('/change-password')
    
    # Should redirect to login
    assert response.status_code == 302
    assert '/login' in response.location


@pytest.mark.unit
def test_change_password_page_loads(auth_client):
    """Test that change password page loads for authenticated users."""
    response = auth_client.get('/change-password')
    
    assert response.status_code == 200
    assert b'password' in response.data.lower()


@pytest.mark.unit
def test_security_headers(client):
    """Test that security headers are present."""
    response = client.get('/login')
    
    assert 'X-Frame-Options' in response.headers
    assert 'X-Content-Type-Options' in response.headers
    assert 'Content-Security-Policy' in response.headers
    assert 'Referrer-Policy' in response.headers


@pytest.mark.unit
def test_authenticated_user_redirects_from_login(auth_client):
    """Test that authenticated users are redirected from login page."""
    response = auth_client.get('/login', follow_redirects=False)
    
    assert response.status_code == 302
    assert response.location == '/'

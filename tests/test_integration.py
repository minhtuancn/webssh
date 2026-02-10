"""Integration tests for the application."""
import pytest


@pytest.mark.integration
def test_full_user_flow(client):
    """Test complete user registration, login, and logout flow."""
    # Register
    response = client.post('/register', data={
        'username': 'flowuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Logout
    response = client.post('/logout', follow_redirects=True)
    assert response.status_code == 200
    
    # Login
    response = client.post('/login', data={
        'username': 'flowuser',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Access protected page
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.integration
def test_password_change_flow(auth_client):
    """Test password change flow."""
    # Change password
    response = auth_client.post('/change-password', data={
        'current_password': 'testpassword123',
        'new_password': 'newpassword456',
        'confirm_password': 'newpassword456'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Logout
    auth_client.post('/logout')
    
    # Try to login with old password (should fail)
    response = auth_client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword123'
    })
    assert b'Invalid' in response.data
    
    # Login with new password (should succeed)
    response = auth_client.post('/login', data={
        'username': 'testuser',
        'password': 'newpassword456'
    }, follow_redirects=True)
    assert response.status_code == 200

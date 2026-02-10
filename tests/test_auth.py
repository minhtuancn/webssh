"""Unit tests for authentication functionality."""
import pytest
from app.models import User, db


@pytest.mark.unit
def test_user_model_password_hashing(app):
    """Test that passwords are properly hashed."""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('securepassword')
        
        assert user.password_hash is not None
        assert user.password_hash != 'securepassword'
        assert user.check_password('securepassword')
        assert not user.check_password('wrongpassword')


@pytest.mark.unit
def test_user_registration(client):
    """Test user registration."""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # User is redirected to index page after successful registration
    assert b'Web SSH Terminal' in response.data


@pytest.mark.unit
def test_user_registration_password_mismatch(client):
    """Test registration with mismatched passwords."""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password123',
        'confirm_password': 'differentpassword'
    })
    
    assert response.status_code == 200
    assert b'do not match' in response.data


@pytest.mark.unit
def test_user_login(client):
    """Test user login."""
    # First register a user
    client.post('/register', data={
        'username': 'loginuser',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    # Logout
    client.post('/logout')
    
    # Try to login
    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200


@pytest.mark.unit
def test_user_login_wrong_password(client):
    """Test login with wrong password."""
    # First register a user
    client.post('/register', data={
        'username': 'testuser2',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    
    # Logout
    client.post('/logout')
    
    # Try to login with wrong password
    response = client.post('/login', data={
        'username': 'testuser2',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data


@pytest.mark.unit
def test_user_logout(auth_client):
    """Test user logout."""
    response = auth_client.post('/logout', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'login' in response.data.lower()


@pytest.mark.unit
def test_password_change(auth_client):
    """Test password change functionality."""
    response = auth_client.post('/change-password', data={
        'current_password': 'testpassword123',
        'new_password': 'newpassword123',
        'confirm_password': 'newpassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200


@pytest.mark.unit
def test_password_change_wrong_current(auth_client):
    """Test password change with wrong current password."""
    response = auth_client.post('/change-password', data={
        'current_password': 'wrongpassword',
        'new_password': 'newpassword123',
        'confirm_password': 'newpassword123'
    })
    
    assert response.status_code == 200
    assert b'Current password is incorrect' in response.data

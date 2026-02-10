"""Test configuration and fixtures."""
import pytest
import os
import tempfile

# Set environment variables BEFORE importing app
os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'
os.environ['CORS_ORIGINS'] = 'http://localhost:5000'
os.environ['DEBUG'] = 'True'
os.environ['RATELIMIT_ENABLED'] = 'False'

from app import create_app, db


@pytest.fixture
def app():
    """Create and configure a test instance of the app."""
    # Create a temporary directory for test data
    test_data_dir = tempfile.mkdtemp()
    
    # Set test environment variables
    os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'
    os.environ['CORS_ORIGINS'] = 'http://localhost:5000'
    os.environ['DEBUG'] = 'True'
    os.environ['DATA_DIR'] = test_data_dir
    os.environ['RATELIMIT_ENABLED'] = 'False'  # Disable rate limiting in tests
    
    # Create the app with test config
    app = create_app()
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    
    # Create the database and tables
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()


@pytest.fixture
def auth_client(client):
    """A test client with an authenticated user."""
    # Register and login a test user
    client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword123',
        'confirm_password': 'testpassword123'
    })
    
    # Login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpassword123'
    })
    
    return client

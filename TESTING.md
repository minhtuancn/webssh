# Testing Guide for WebSSH

This document provides instructions for running tests in the WebSSH project.

## Test Infrastructure

The project uses **pytest** as the testing framework with the following plugins:
- `pytest-cov`: For code coverage reporting
- `pytest-flask`: For Flask application testing
- `pytest-mock`: For mocking functionality

## Setup

### 1. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (includes testing tools)
pip install -r requirements-dev.txt
```

### 2. Environment Variables

Tests automatically set required environment variables. No manual configuration needed.

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Verbose Output

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
pytest tests/test_routes.py
pytest tests/test_config.py
pytest tests/test_integration.py
```

### Run Tests with Coverage Report

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Run Tests with HTML Coverage Report

```bash
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in your browser to view the report
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest tests/ -m unit

# Run only integration tests
pytest tests/ -m integration
```

## Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── test_auth.py             # Authentication tests
├── test_routes.py           # Route/endpoint tests
├── test_config.py           # Configuration tests
└── test_integration.py      # Integration tests
```

## Test Categories

### Unit Tests (marked with `@pytest.mark.unit`)
- Test individual functions and components in isolation
- Fast execution
- No external dependencies

### Integration Tests (marked with `@pytest.mark.integration`)
- Test multiple components working together
- Test complete user flows
- May be slower than unit tests

## Test Coverage

Current test coverage includes:
- ✅ User authentication (registration, login, logout)
- ✅ Password management (hashing, changing)
- ✅ Route protection (authentication required)
- ✅ Security headers
- ✅ Configuration validation
- ✅ User flows (registration → login → logout)

## Continuous Integration

Tests are automatically run in CI/CD pipelines. The project uses GitHub Actions for automated testing.

## Writing New Tests

### Example Test Structure

```python
import pytest

@pytest.mark.unit
def test_example(client):
    """Test description."""
    # Arrange
    data = {'key': 'value'}
    
    # Act
    response = client.post('/endpoint', data=data)
    
    # Assert
    assert response.status_code == 200
    assert b'expected' in response.data
```

### Using Fixtures

```python
def test_with_auth(auth_client):
    """Test with authenticated user."""
    response = auth_client.get('/protected-route')
    assert response.status_code == 200
```

Available fixtures:
- `app`: Flask application instance
- `client`: Test client for making requests
- `runner`: CLI test runner
- `auth_client`: Test client with authenticated user

## Code Quality

### Run Linter

```bash
flake8 .
```

### Format Code

```bash
black .
```

## Troubleshooting

### Tests Fail with Database Errors
- Tests use an in-memory SQLite database
- Database is automatically created and cleaned up for each test
- If issues persist, check `conftest.py` fixture configuration

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements-dev.txt`
- Activate virtual environment: `source venv/bin/activate`

### Environment Variable Errors
- Tests automatically set required environment variables
- Check `conftest.py` for environment variable configuration

## Best Practices

1. **Write descriptive test names** that explain what is being tested
2. **Use docstrings** to document test purpose
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Keep tests independent**: Each test should be able to run alone
5. **Use appropriate markers**: Tag tests with `@pytest.mark.unit` or `@pytest.mark.integration`
6. **Mock external dependencies**: Don't make real SSH connections in tests
7. **Clean up after tests**: Use fixtures for setup and teardown

## Current Test Results

All 25 tests pass successfully:

```
tests/test_auth.py ................  (8 tests)
tests/test_config.py .............  (7 tests)
tests/test_integration.py ......... (2 tests)
tests/test_routes.py .............. (8 tests)

======================== 25 passed in 8.45s =========================
```

## Future Testing Improvements

Potential areas for expanded test coverage:
- SSH connection management
- SFTP file operations
- WebSocket event handlers
- Session management
- Rate limiting
- Key encryption/decryption
- Command library functionality
- Profile management

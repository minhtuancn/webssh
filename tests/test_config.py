"""Unit tests for configuration."""
import pytest
import os
import config


@pytest.mark.unit
def test_config_debug_mode():
    """Test DEBUG configuration."""
    assert config.DEBUG in [True, False]


@pytest.mark.unit
def test_config_secret_key_exists():
    """Test that SECRET_KEY is set."""
    assert config.SECRET_KEY is not None
    assert len(config.SECRET_KEY) > 0


@pytest.mark.unit
def test_config_session_timeout():
    """Test session timeout configuration."""
    assert config.SESSION_TIMEOUT > 0
    assert isinstance(config.SESSION_TIMEOUT, int)


@pytest.mark.unit
def test_config_max_sessions():
    """Test max sessions configuration."""
    assert config.MAX_SESSIONS > 0
    assert config.MAX_SESSIONS <= 20


@pytest.mark.unit
def test_config_password_length():
    """Test minimum password length configuration."""
    assert config.MIN_PASSWORD_LENGTH >= 8


@pytest.mark.unit
def test_config_cors_origins():
    """Test CORS origins configuration."""
    assert config.CORS_ORIGINS is not None


@pytest.mark.unit
def test_config_data_dir_exists():
    """Test that data directory path is configured."""
    assert config.DATA_DIR is not None

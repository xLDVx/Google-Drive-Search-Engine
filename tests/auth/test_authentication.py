import os
import json
import pytest
from auth.authentication import AuthenticationManager

@pytest.fixture
def mock_client_id(tmp_path):
    """
    Create a temporary client ID configuration file.
    
    Args:
        tmp_path: Pytest temporary directory fixture
    
    Returns:
        str: Path to the temporary client ID file
    """
    client_id_data = {
        "client_id": "test_client_id",
        "client_secret": "test_client_secret"
    }
    client_id_path = tmp_path / "client_id.json"
    with open(client_id_path, 'w') as f:
        json.dump(client_id_data, f)
    return str(client_id_path)

@pytest.fixture
def mock_credentials(tmp_path):
    """
    Create a temporary credentials configuration file.
    
    Args:
        tmp_path: Pytest temporary directory fixture
    
    Returns:
        str: Path to the temporary credentials file
    """
    credentials_data = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token"
    }
    credentials_path = tmp_path / "credentials.json"
    with open(credentials_path, 'w') as f:
        json.dump(credentials_data, f)
    return str(credentials_path)

@pytest.mark.auth
def test_get_client_id(mock_client_id):
    """
    Test retrieving client ID configuration.
    """
    auth_manager = AuthenticationManager(client_id_path=mock_client_id)
    client_id = auth_manager.get_client_id()
    
    assert client_id is not None
    assert "client_id" in client_id
    assert "client_secret" in client_id
    assert client_id["client_id"] == "test_client_id"

@pytest.mark.auth
def test_get_credentials(mock_credentials):
    """
    Test retrieving credentials.
    """
    auth_manager = AuthenticationManager(credentials_path=mock_credentials)
    credentials = auth_manager.get_credentials()
    
    assert credentials is not None
    assert "access_token" in credentials
    assert "refresh_token" in credentials
    assert credentials["access_token"] == "test_access_token"

@pytest.mark.auth
def test_token_validity(mock_credentials):
    """
    Test token validity checking.
    """
    auth_manager = AuthenticationManager(credentials_path=mock_credentials)
    
    assert auth_manager.is_token_valid() is True

@pytest.mark.auth
def test_invalid_client_id_file(tmp_path):
    """
    Test handling of invalid client ID file.
    """
    invalid_client_id_path = tmp_path / "invalid_client_id.json"
    with open(invalid_client_id_path, 'w') as f:
        f.write("Invalid JSON")
    
    auth_manager = AuthenticationManager(client_id_path=str(invalid_client_id_path))
    
    with pytest.raises(ValueError, match="Invalid client ID JSON configuration"):
        auth_manager.get_client_id()

@pytest.mark.auth
def test_missing_credentials_file(tmp_path):
    """
    Test handling of missing credentials file.
    """
    non_existent_path = tmp_path / "non_existent_credentials.json"
    auth_manager = AuthenticationManager(credentials_path=str(non_existent_path))
    
    assert auth_manager.get_credentials() is None
    assert auth_manager.is_token_valid() is False
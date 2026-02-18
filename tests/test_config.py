"""
Testes para configuração
"""
import pytest
import tempfile
import os
from pathlib import Path
from generator.config import Config, load_demo_config


def test_load_demo_config():
    """Testa carregamento de config demo"""
    config = load_demo_config()
    assert config.username == "EuHttl"
    assert config.profile["name"] == "Hyttalo Costa"
    assert len(config.galaxy_arms) == 3


def test_config_validation_missing_username():
    """Testa validação de username obrigatório"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write("profile:\n  name: Test\n")
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError, match="username"):
            Config(temp_path)
    finally:
        os.unlink(temp_path)


def test_config_validation_missing_name():
    """Testa validação de profile.name obrigatório"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write("username: testuser\n")
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError, match="profile.name"):
            Config(temp_path)
    finally:
        os.unlink(temp_path)


def test_config_theme_defaults():
    """Testa que tema usa valores padrão quando não especificado"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write("username: testuser\nprofile:\n  name: Test User\n")
        temp_path = f.name
    
    try:
        config = Config(temp_path)
        theme = config.theme
        assert theme["void_black"] == "#0a0e27"
        assert theme["synapse_cyan"] == "#00d9ff"
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

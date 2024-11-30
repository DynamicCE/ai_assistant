import pytest
from src.utils.config import Config
import os

def test_config_validation():
    os.environ['CLAUDE_API_KEY'] = ''
    os.environ['ELEVENLABS_API_KEY'] = ''
    
    with pytest.raises(ValueError):
        Config()

def test_config_wake_word():
    os.environ['CLAUDE_API_KEY'] = 'test'
    os.environ['ELEVENLABS_API_KEY'] = 'test'
    os.environ['WAKE_WORD'] = 'merhaba asistan'
    
    config = Config()
    assert config.wake_word == 'merhaba asistan' 
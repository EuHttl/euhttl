"""
Testes básicos para o Galaxy Profile Generator
"""
import pytest
from generator.utils import (
    escape_xml,
    format_number,
    hex_to_rgb,
    get_language_color,
)


def test_escape_xml():
    """Testa escape de caracteres XML"""
    assert escape_xml("Hello & goodbye") == "Hello &amp; goodbye"
    assert escape_xml("<tag>") == "&lt;tag&gt;"
    assert escape_xml('Say "hi"') == 'Say &quot;hi&quot;'
    assert escape_xml("It's") == "It&apos;s"


def test_format_number():
    """Testa formatação de números"""
    assert format_number(500) == "500"
    assert format_number(1500) == "1.5K"
    assert format_number(1000000) == "1.0M"
    assert format_number(2500000) == "2.5M"


def test_hex_to_rgb():
    """Testa conversão hex para RGB"""
    assert hex_to_rgb("#ffffff") == (255, 255, 255)
    assert hex_to_rgb("#000000") == (0, 0, 0)
    assert hex_to_rgb("#ff0000") == (255, 0, 0)
    assert hex_to_rgb("00ff00") == (0, 255, 0)


def test_get_language_color():
    """Testa cores de linguagens"""
    assert get_language_color("Python") == "#3572A5"
    assert get_language_color("JavaScript") == "#f1e05a"
    assert get_language_color("TypeScript") == "#2b7489"
    assert get_language_color("UnknownLang") == "#858585"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

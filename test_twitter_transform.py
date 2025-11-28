#!/usr/bin/env python3
"""
Tests unitaires pour twitter_transform.py
"""

import pytest
from transforms.twitter_transform import validate_twitter_alias


def test_valid_alias():
    """Test avec un alias valide standard"""
    valid, cleaned, err = validate_twitter_alias("elonmusk")
    assert valid == True
    assert cleaned == "elonmusk"
    assert err == ""


def test_alias_with_at():
    """Test avec le préfixe @ (doit être nettoyé)"""
    valid, cleaned, err = validate_twitter_alias("@snowden")
    assert valid == True
    assert cleaned == "snowden"
    assert err == ""


def test_alias_with_spaces():
    """Test avec des espaces (doivent être nettoyés)"""
    valid, cleaned, err = validate_twitter_alias("  user_123  ")
    assert valid == True
    assert cleaned == "user_123"
    assert err == ""


def test_alias_with_at_and_spaces():
    """Test combiné @ et espaces"""
    valid, cleaned, err = validate_twitter_alias("  @test_user  ")
    assert valid == True
    assert cleaned == "test_user"
    assert err == ""


def test_invalid_chars_dash():
    """Test avec tiret (invalide)"""
    valid, cleaned, err = validate_twitter_alias("user-name")
    assert valid == False
    assert cleaned == "user-name"
    assert "caractères invalides" in err


def test_invalid_chars_special():
    """Test avec caractères spéciaux"""
    valid, cleaned, err = validate_twitter_alias("user@domain.com")
    assert valid == False
    assert "caractères invalides" in err


def test_too_long():
    """Test avec alias trop long (> 15 caractères)"""
    long_alias = "a" * 20
    valid, cleaned, err = validate_twitter_alias(long_alias)
    assert valid == False
    assert cleaned == long_alias
    assert "trop long" in err


def test_max_length():
    """Test avec exactement 15 caractères (limite)"""
    alias_15 = "a" * 15
    valid, cleaned, err = validate_twitter_alias(alias_15)
    assert valid == True
    assert cleaned == alias_15
    assert err == ""


def test_reserved_name_settings():
    """Test avec nom réservé 'settings'"""
    valid, cleaned, err = validate_twitter_alias("settings")
    assert valid == False
    assert cleaned == "settings"
    assert "réservé" in err


def test_reserved_name_mentions():
    """Test avec nom réservé 'mentions'"""
    valid, cleaned, err = validate_twitter_alias("mentions")
    assert valid == False
    assert "réservé" in err


def test_reserved_name_case_insensitive():
    """Test que la vérification des noms réservés est insensible à la casse"""
    valid, cleaned, err = validate_twitter_alias("SETTINGS")
    assert valid == False
    assert "réservé" in err


def test_empty_string():
    """Test avec chaîne vide"""
    valid, cleaned, err = validate_twitter_alias("")
    assert valid == False
    assert cleaned == ""
    assert "vide" in err


def test_only_at_symbol():
    """Test avec seulement le symbole @"""
    valid, cleaned, err = validate_twitter_alias("@")
    assert valid == False
    assert cleaned == ""
    assert "caractères invalides" in err


def test_numbers_only():
    """Test avec seulement des chiffres (valide)"""
    valid, cleaned, err = validate_twitter_alias("123456")
    assert valid == True
    assert cleaned == "123456"
    assert err == ""


def test_underscore_only():
    """Test avec seulement des underscores (valide selon Twitter)"""
    valid, cleaned, err = validate_twitter_alias("___")
    assert valid == True
    assert cleaned == "___"
    assert err == ""


def test_mixed_alphanumeric():
    """Test avec mélange de lettres, chiffres et underscores"""
    valid, cleaned, err = validate_twitter_alias("User_123_Test")
    assert valid == True
    assert cleaned == "User_123_Test"
    assert err == ""


def test_none_value():
    """Test avec None (edge case)"""
    # Twitter_transform attend une string, mais on teste la robustesse
    # Note: Ce test pourrait lever une exception selon l'implémentation
    try:
        valid, cleaned, err = validate_twitter_alias(None)
        # Si aucune exception, on vérifie que c'est invalide
        assert valid == False
    except (AttributeError, TypeError):
        # Attendu si None.strip() est appelé
        pass


if __name__ == "__main__":
    # Exécuter les tests avec pytest
    print("Exécution des tests pour twitter_transform.py...")
    pytest.main([__file__, "-v", "--tb=short"])

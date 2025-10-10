# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the abstract API manager utilities."""


from multisafepay.api.base.abstract_manager import AbstractManager


def test_encode_path_segment_with_normal_string():
    """Test encoding a normal string without special characters."""
    result = AbstractManager.encode_path_segment("normal_string")
    assert result == "normal_string"


def test_encode_path_segment_with_spaces():
    """Test encoding a string with spaces."""
    result = AbstractManager.encode_path_segment("hello world")
    assert result == "hello%20world"


def test_encode_path_segment_with_special_characters():
    """Test encoding a string with various special characters."""
    result = AbstractManager.encode_path_segment("hello@world#test")
    assert result == "hello%40world%23test"


def test_encode_path_segment_with_forward_slash():
    """Test encoding a string with forward slashes."""
    result = AbstractManager.encode_path_segment("path/to/resource")
    assert result == "path%2Fto%2Fresource"


def test_encode_path_segment_with_question_mark():
    """Test encoding a string with question marks."""
    result = AbstractManager.encode_path_segment("query?param=value")
    assert result == "query%3Fparam%3Dvalue"


def test_encode_path_segment_with_ampersand():
    """Test encoding a string with ampersands."""
    result = AbstractManager.encode_path_segment("param1&param2")
    assert result == "param1%26param2"


def test_encode_path_segment_with_equals_sign():
    """Test encoding a string with equals signs."""
    result = AbstractManager.encode_path_segment("key=value")
    assert result == "key%3Dvalue"


def test_encode_path_segment_with_percentage_sign():
    """Test encoding a string with percentage signs."""
    result = AbstractManager.encode_path_segment("discount%off")
    assert result == "discount%25off"


def test_encode_path_segment_with_plus_sign():
    """Test encoding a string with plus signs."""
    result = AbstractManager.encode_path_segment("one+two")
    assert result == "one%2Btwo"


def test_encode_path_segment_with_unicode_characters():
    """Test encoding a string with Unicode characters."""
    result = AbstractManager.encode_path_segment("café")
    assert result == "caf%C3%A9"


def test_encode_path_segment_with_emoji():
    """Test encoding a string with emoji characters."""
    result = AbstractManager.encode_path_segment("hello😊world")
    assert result == "hello%F0%9F%98%8Aworld"


def test_encode_path_segment_with_empty_string():
    """Test encoding an empty string."""
    result = AbstractManager.encode_path_segment("")
    assert result == ""


def test_encode_path_segment_with_only_special_characters():
    """Test encoding a string with only special characters."""
    result = AbstractManager.encode_path_segment("!@#$%^&*()")
    assert result == "%21%40%23%24%25%5E%26%2A%28%29"


def test_encode_path_segment_with_numbers():
    """Test encoding a string with numbers."""
    result = AbstractManager.encode_path_segment("123456")
    assert result == "123456"


def test_encode_path_segment_with_mixed_alphanumeric():
    """Test encoding a string with mixed alphanumeric characters."""
    result = AbstractManager.encode_path_segment("abc123XYZ")
    assert result == "abc123XYZ"


def test_encode_path_segment_with_hyphen_and_underscore():
    """Test encoding a string with hyphens and underscores (safe characters)."""
    result = AbstractManager.encode_path_segment("test-value_123")
    assert result == "test-value_123"


def test_encode_path_segment_with_period_and_tilde():
    """Test encoding a string with periods and tildes (safe characters)."""
    result = AbstractManager.encode_path_segment("file.txt~backup")
    assert result == "file.txt~backup"


def test_encode_path_segment_with_integer_input():
    """Test encoding an integer input (should be converted to string)."""
    result = AbstractManager.encode_path_segment(12345)
    assert result == "12345"


def test_encode_path_segment_with_float_input():
    """Test encoding a float input (should be converted to string)."""
    result = AbstractManager.encode_path_segment(123.45)
    assert result == "123.45"


def test_encode_path_segment_with_none_input():
    """Test encoding None input (should be converted to string)."""
    result = AbstractManager.encode_path_segment(None)
    assert result == "None"


def test_encode_path_segment_preserves_unreserved_characters():
    """Test that unreserved characters are not encoded."""
    # RFC 3986 unreserved characters: ALPHA / DIGIT / "-" / "." / "_" / "~"
    unreserved = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    )
    result = AbstractManager.encode_path_segment(unreserved)
    assert result == unreserved


def test_encode_path_segment_encodes_reserved_characters():
    """Test that reserved characters are properly encoded."""
    # Some RFC 3986 reserved characters
    reserved = ":/?#[]@!$&'()*+,;="
    result = AbstractManager.encode_path_segment(reserved)
    # All characters should be encoded since safe="" is used
    assert ":" not in result
    assert "/" not in result
    assert "?" not in result
    assert "#" not in result
    assert "@" not in result
    assert "!" not in result
    assert "$" not in result
    assert "&" not in result
    assert "'" not in result
    assert "(" not in result
    assert ")" not in result
    assert "*" not in result
    assert "+" not in result
    assert "," not in result
    assert ";" not in result
    assert "=" not in result

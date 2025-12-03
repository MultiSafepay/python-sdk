# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Unit tests for the shared description model."""


from multisafepay.api.shared.description import Description


def test_initializes_with_default_values():
    """Test that a Description instance initializes with default values."""
    description = Description()
    assert description.description is None


def test_adds_description_text():
    """Test that a description text is added to the Description instance."""
    description = Description().add_description("Sample description")
    assert description.description == "Sample description"


def test_gets_description_text():
    """Test that the description text is retrieved from the Description instance."""
    description = Description().add_description("Sample description")
    assert description.get() == "Sample description"


def test_strips_html_tags():
    """Test that HTML tags are stripped from a given text."""
    text = "<p>This is a <strong>test</strong> description.</p>"
    stripped_text = Description.strip_tags(text)
    assert stripped_text == "This is a test description."


def test_creates_from_text():
    """Test that a Description instance is created from a given text."""
    description = Description.from_text("Sample description")
    assert description.description == "Sample description"

# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.google_analytics import (
    GoogleAnalytics,
)


def test_initializes_google_analytics_correctly():
    """Tests that the GoogleAnalytics object is initialized correctly with the given account ID."""
    google_analytics = GoogleAnalytics(account_id="UA-12345678-1")

    assert google_analytics.account_id == "UA-12345678-1"


def test_initializes_google_analytics_with_empty_value():
    """Tests that the GoogleAnalytics object is initialized with None when no account ID is provided."""
    google_analytics = GoogleAnalytics()

    assert google_analytics.account_id is None


def test_add_account_id_updates_value():
    """Tests that the add_account_id method updates the account_id field correctly."""
    google_analytics = GoogleAnalytics()
    google_analytics_updated = google_analytics.add_account_id("UA-12345678-1")

    assert google_analytics.account_id == "UA-12345678-1"
    assert isinstance(google_analytics_updated, GoogleAnalytics)

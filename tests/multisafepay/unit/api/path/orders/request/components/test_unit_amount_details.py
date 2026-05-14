"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.amount_details import (
    AmountDetails,
)
from multisafepay.api.paths.orders.request.components.tip import Tip


def test_initializes_amount_details_correctly():
    """Test that AmountDetails initializes correctly with all parameters."""
    tip = Tip(amount=20)
    amount_details = AmountDetails(tip=tip)

    assert amount_details.tip == tip


def test_initializes_amount_details_with_empty_values():
    """Test that AmountDetails initializes with None values when no parameters are provided."""
    amount_details = AmountDetails()

    assert amount_details.tip is None


def test_add_tip_updates_value():
    """Test that add_tip updates the tip value."""
    amount_details = AmountDetails()
    tip = Tip(amount=20)
    amount_details_updated = amount_details.add_tip(tip)

    assert amount_details.tip == tip
    assert isinstance(amount_details_updated, AmountDetails)


def test_amount_details_to_dict_serializes_tip():
    """Test that to_dict serializes tip information without null fields."""
    amount_details = AmountDetails(tip=Tip(amount=20))

    assert amount_details.to_dict() == {"tip": {"amount": 20}}

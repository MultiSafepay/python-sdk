"""Test module for unit testing."""

from multisafepay.api.paths.orders.request.components.tip import Tip
from multisafepay.value_object.amount import Amount


def test_initializes_tip_correctly():
    """Test that Tip initializes correctly with all parameters."""
    tip = Tip(amount=20)

    assert tip.amount == 20


def test_initializes_tip_with_empty_values():
    """Test that Tip initializes with None values when no parameters are provided."""
    tip = Tip()

    assert tip.amount is None


def test_add_tip_amount_updates_value():
    """Test that add_amount updates the tip amount value."""
    tip = Tip()
    tip_updated = tip.add_amount(20)

    assert tip.amount == 20
    assert isinstance(tip_updated, Tip)


def test_add_tip_amount_accepts_amount_value_object():
    """Test that add_amount accepts an Amount value object."""
    tip = Tip()
    tip_updated = tip.add_amount(Amount(amount=20))

    assert tip.amount == 20
    assert isinstance(tip_updated, Tip)


def test_add_tip_amount_accepts_none():
    """Test that add_amount accepts None."""
    tip = Tip(amount=20)
    tip_updated = tip.add_amount(None)

    assert tip.amount is None
    assert isinstance(tip_updated, Tip)

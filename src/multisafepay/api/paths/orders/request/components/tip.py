"""Tip model for order request amount details."""

from typing import Optional, Union

from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.amount import Amount


class Tip(RequestModel):
    """
    Represents tip information in order amount details.

    Attributes
    ----------
    amount (Optional[int]): The tip amount in the smallest currency unit.

    """

    amount: Optional[int]

    def add_amount(
        self: "Tip",
        amount: Optional[Union[Amount, int]],
    ) -> "Tip":
        """
        Adds the tip amount.

        Parameters
        ----------
        amount (Optional[Amount | int]): The tip amount as an Amount object or integer.

        Returns
        -------
        Tip: The updated Tip object.

        """
        if isinstance(amount, int):
            amount = Amount(amount=amount)
        self.amount = amount.get() if amount is not None else None
        return self

"""Amount details model for order request amount breakdowns."""

from typing import Optional

from multisafepay.api.paths.orders.request.components.tip import Tip
from multisafepay.model.request_model import RequestModel


class AmountDetails(RequestModel):
    """
    Represents amount details for an order request.

    Attributes
    ----------
    tip (Optional[Tip]): The tip information.

    """

    tip: Optional[Tip]

    def add_tip(
        self: "AmountDetails",
        tip: Optional[Tip],
    ) -> "AmountDetails":
        """
        Adds tip information to the amount details.

        Parameters
        ----------
        tip (Optional[Tip]): The tip information.

        Returns
        -------
        AmountDetails: The updated AmountDetails object.

        """
        self.tip = tip
        return self

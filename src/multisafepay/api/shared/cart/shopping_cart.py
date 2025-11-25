# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Shopping cart model for managing cart items in order processing."""

from typing import List, Optional

from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.model.api_model import ApiModel


class ShoppingCart(ApiModel):
    """
    A class to represent a shopping cart.

    Attributes
    ----------
    items: (Optional[List[CartItem]]) The list of items in the shopping cart.

    """

    items: Optional[List[CartItem]]

    def get_items(self: "ShoppingCart") -> Optional[List[CartItem]]:
        """
        Get the list of items in the shopping cart.

        Returns
        -------
        Optional[List[CartItem]]: The list of items in the shopping cart, or None if no items exist.

        """
        return self.items

    def add_items(
        self: "ShoppingCart",
        items: Optional[List[CartItem]],
    ) -> "ShoppingCart":
        """
        Add multiple items to the shopping cart.

        Parameters
        ----------
        items: (Optional[List[CartItem]]) The list of items to be added to the shopping cart.

        Returns
        -------
        ShoppingCart: The updated ShoppingCart instance.

        """
        if items is not None:
            self.items = items
        return self

    def add_item(
        self: "ShoppingCart",
        item: Optional[CartItem],
    ) -> "ShoppingCart":
        """
        Add a single item to the shopping cart.

        Parameters
        ----------
        item: (Optional[CartItem]) The item to be added to the shopping cart.

        Returns
        -------
        ShoppingCart: The updated ShoppingCart instance.

        """
        if item is None:
            return self
        if self.items is None:
            self.items = []
        self.items.append(item)
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["ShoppingCart"]:
        """
        Create a ShoppingCart instance from a dictionary.

        Parameters
        ----------
        d: (Optional[dict]) A dictionary containing the shopping cart data, by default None.

        Returns
        -------
        Optional[ShoppingCart]: A ShoppingCart instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None

        if d.get("items") is None:
            return ShoppingCart(items=None)

        return ShoppingCart(
            items=[CartItem.from_dict(item) for item in d.get("items", [])],
        )

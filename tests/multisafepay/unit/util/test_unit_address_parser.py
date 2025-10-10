# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


"""Utility functions for test unit address parser."""

import pytest
from multisafepay.util.address_parser import AddressParser


class TestAddressParser:
    """Test class for AddressParser functionality."""

    @pytest.mark.parametrize(
        ("address1", "address2", "expected_street", "expected_apartment"),
        [
            (
                "Kraanspoor",
                "39",
                "Kraanspoor",
                "39",
            ),
            (
                "Kraanspoor ",
                "39",
                "Kraanspoor",
                "39",
            ),
            (
                "Kraanspoor 39",
                "",
                "Kraanspoor",
                "39",
            ),
            (
                "Kraanspoor 39 ",
                "",
                "Kraanspoor",
                "39",
            ),
            (
                "Kraanspoor",
                "39 ",
                "Kraanspoor",
                "39",
            ),
            (
                "Kraanspoor39",
                "",
                "Kraanspoor",
                "39",
            ),
            (
                "Kraanspoor39c",
                "",
                "Kraanspoor",
                "39c",
            ),
            (
                "laan 1933 2",
                "",
                "laan 1933",
                "2",
            ),
            (
                "laan 1933",
                "2",
                "laan 1933",
                "2",
            ),
            (
                "18 septemberplein 12",
                "",
                "18 septemberplein",
                "12",
            ),
            (
                "18 septemberplein",
                "12",
                "18 septemberplein",
                "12",
            ),
            (
                "kerkstraat 42-f3",
                "",
                "kerkstraat",
                "42-f3",
            ),
            (
                "kerkstraat",
                "42-f3",
                "kerkstraat",
                "42-f3",
            ),
            (
                "Kerk straat 2b",
                "",
                "Kerk straat",
                "2b",
            ),
            (
                "Kerk straat",
                "2b",
                "Kerk straat",
                "2b",
            ),
            (
                "1e constantijn huigensstraat 1b",
                "",
                "1e constantijn huigensstraat",
                "1b",
            ),
            (
                "1e constantijn huigensstraat",
                "1b",
                "1e constantijn huigensstraat",
                "1b",
            ),
            (
                "Heuvel, 2a",
                "",
                "Heuvel,",
                "2a",
            ),
            (
                "1e Jan  van  Kraanspoor",
                "2",
                "1e Jan van Kraanspoor",
                "2",
            ),
            (
                "Neherkade 1 XI",
                "",
                "Neherkade",
                "1 XI",
            ),
            (
                "Kamp 20 38",
                "",
                "Kamp 20",
                "38",
            ),
            (
                "2065 Rue de la Gare",
                "",
                "Rue de la Gare",
                "2065",
            ),
            (
                "10 Downing Street",
                "",
                "Downing Street",
                "10",
            ),
            (
                "27",
                "Alexander Road",
                "Alexander Road",
                "27",
            ),
            (
                "15 Sullivan",
                "",
                "Sullivan",
                "15",
            ),
            (
                "110 Kraanspoor",
                "",
                "Kraanspoor",
                "110",
            ),
            (
                "Plaza Callao s/n",
                "",
                "Plaza Callao s/n",
                "",
            ),
        ],
    )
    def test_parse_addresses_from_data_provider(
        self: "TestAddressParser",
        address1: str,
        address2: str,
        expected_street: str,
        expected_apartment: str,
    ) -> None:
        """
        Test the function parse with a provider, to confirm all addresses work.

        Args:
        ----
            address1: Primary address line
            address2: Secondary address line
            expected_street: Expected street name result
            expected_apartment: Expected apartment/house number result

        """
        parser = AddressParser()
        result = parser.parse(address1, address2)

        assert (
            result[0] == expected_street
        ), f"Street mismatch: expected '{expected_street}', got '{result[0]}'"
        assert (
            result[1] == expected_apartment
        ), f"Apartment mismatch: expected '{expected_apartment}', got '{result[1]}'"

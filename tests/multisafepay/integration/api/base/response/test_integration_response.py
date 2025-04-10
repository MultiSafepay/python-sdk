# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.listings.pager import Pager


def test_get_pager_returns_pager():
    """
    Test that get_pager returns the correct pager object from the response body.

    Raises
    ------
    AssertionError
        If the returned pager object does not match the expected value.

    """
    pager = Pager(after="next", before="prev", limit=10, cursor=None)
    response = ApiResponse(
        status_code=200,
        body={"pager": pager},
        context={},
        headers={},
        raw="",
    )
    assert response.get_pager() == pager

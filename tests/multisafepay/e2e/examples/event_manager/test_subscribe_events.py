# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""E2E coverage for examples/event_manager/subscribe_events.py."""

import time

import pytest

from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.events.event_manager import EventManager
from multisafepay.api.paths.events.stream import EventStream
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.orders.request.order_request import OrderRequest
from multisafepay.api.paths.orders.response.order_response import Order
from multisafepay.sdk import Sdk


@pytest.fixture(scope="module")
def order_manager(cloud_pos_events_sdk: Sdk) -> OrderManager:
    """Return OrderManager for Cloud POS event-stream tests."""
    return cloud_pos_events_sdk.get_order_manager()


@pytest.fixture(scope="module")
def event_manager(cloud_pos_events_sdk: Sdk) -> EventManager:
    """Return EventManager for Cloud POS event-stream tests."""
    return cloud_pos_events_sdk.get_event_manager()


def _build_cloud_pos_order_request(
    order_id: str,
    terminal_id: str,
) -> OrderRequest:
    """Create the Cloud POS order request used by the SSE example."""
    return (
        OrderRequest()
        .add_type("redirect")
        .add_order_id(order_id)
        .add_description("Cloud POS order for event streaming")
        .add_amount(100)
        .add_currency("EUR")
        .add_gateway_info(
            {
                "terminal_id": terminal_id,
            },
        )
    )


def test_subscribe_order_events_opens_stream(
    order_manager: OrderManager,
    event_manager: EventManager,
    cloud_pos_terminal_group_id: str,
    cloud_pos_terminal_id: str,
) -> None:
    """Create a Cloud POS order and verify the SSE stream opens successfully."""
    order_id = f"cloud-pos-events-e2e-{int(time.time())}"

    create_response = order_manager.create(
        request_order=_build_cloud_pos_order_request(
            order_id=order_id,
            terminal_id=cloud_pos_terminal_id,
        ),
        terminal_group_id=cloud_pos_terminal_group_id,
    )

    assert isinstance(create_response, CustomApiResponse)
    assert create_response.get_status_code() == 200
    assert create_response.get_body_success() is True

    order = create_response.get_data()
    assert isinstance(order, Order)
    assert order.order_id == order_id
    assert order.events_token or order.event_token
    assert order.events_stream_url or order.event_stream_url

    with event_manager.subscribe_order_events(order, timeout=10.0) as stream:
        assert isinstance(stream, EventStream)
        assert stream.closed is False

    assert stream.closed is True

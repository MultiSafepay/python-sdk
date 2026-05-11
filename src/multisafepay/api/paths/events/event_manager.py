# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Event manager for event stream subscription helpers."""

from __future__ import annotations

from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.paths.events.stream import EventStream
from multisafepay.api.paths.orders.response.order_response import Order
from multisafepay.client.client import Client


class EventManager(AbstractManager):
    """Manages event stream subscriptions for order events."""

    def __init__(self: EventManager, client: Client) -> None:
        """Initialize the EventManager with a client."""
        super().__init__(client)

    def subscribe_events(
        self: EventManager,
        events_token: str,
        events_stream_url: str,
        last_event_id: str | None = None,
        timeout: float = 30.0,
    ) -> EventStream:
        """
        Subscribe to order events using the SSE stream endpoint.

        Parameters
        ----------
        events_token (str): Token returned by order creation for event auth.
        events_stream_url (str): Full SSE stream URL.
        last_event_id (str | None): Optional resume cursor.
        timeout (float): Socket timeout in seconds.

        Returns
        -------
        EventStream: An iterator over incoming SSE messages.

        """
        return EventStream.open(
            events_token=events_token,
            events_stream_url=events_stream_url,
            last_event_id=last_event_id,
            timeout=timeout,
        )

    def subscribe_order_events(
        self: EventManager,
        order: Order,
        last_event_id: str | None = None,
        timeout: float = 30.0,
    ) -> EventStream:
        """
        Subscribe to events for an existing order response object.

        Parameters
        ----------
        order (Order): Order response that contains event credentials.
        last_event_id (str | None): Optional resume cursor.
        timeout (float): Socket timeout in seconds.

        Returns
        -------
        EventStream: An iterator over incoming SSE messages.

        """
        events_token = order.events_token or order.event_token
        events_stream_url = order.events_stream_url or order.event_stream_url

        if not events_token or not events_stream_url:
            raise ValueError(
                "Order does not contain events_token/events_stream_url.",
            )

        return self.subscribe_events(
            events_token=events_token,
            events_stream_url=events_stream_url,
            last_event_id=last_event_id,
            timeout=timeout,
        )

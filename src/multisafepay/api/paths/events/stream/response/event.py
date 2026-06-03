# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Response models for order event stream messages."""

from __future__ import annotations

from typing import Optional

from multisafepay.api.paths.events.stream.response.components import (
    EventData,
    EventDataPayload,
)
from multisafepay.model.response_model import ResponseModel

# ruff: noqa: UP007


class Event(ResponseModel):
    """Structured event message returned by the MultiSafepay SSE stream."""

    event: Optional[str]
    data: EventDataPayload
    event_id: Optional[str]
    retry: Optional[int]
    raw_data: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional[Event]:
        """Create Event from dictionary data."""
        if d is None:
            return None

        args = d.copy()
        payload = d.get("data")
        if isinstance(payload, dict):
            args["data"] = EventData.from_dict(payload)
        elif isinstance(payload, list):
            args["data"] = [
                EventData.from_dict(item) if isinstance(item, dict) else item
                for item in payload
            ]
        else:
            args["data"] = payload

        return Event(**args)

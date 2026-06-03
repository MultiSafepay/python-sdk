# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

"""Component response models for event stream payloads."""

from __future__ import annotations

from typing import Optional, Union

from multisafepay.model.response_model import ResponseModel

# ruff: noqa: UP007

EventDataPayload = Union[
    "EventData",
    str,
    int,
    float,
    bool,
    list[object],
    None,
]


class EventData(ResponseModel):
    """Structured nested event payload for known order-event attributes."""

    status: Optional[str]
    order_id: Optional[str]
    type: Optional[str]
    data: EventDataPayload

    @staticmethod
    def from_dict(d: dict) -> Optional[EventData]:
        """Create EventData from dictionary data."""
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

        return EventData(**args)

# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import pytest

from multisafepay.util.message import Message, MessageList


def test_message_initialization():
    """
    Test the initialization of a Message object with a specific message content.


    """
    message = Message(message="test message")
    assert message.message == "test message"


def test_message_deserialization():
    """
    Test the deserialization of a Message object to a dictionary.


    """
    message = Message(message="test message")
    assert message.dict() == {"message": "test message"}


def test_empty_message_initialization():
    """
    Test the initialization of a Message object without providing any message content.


    """
    with pytest.raises(ValueError):
        Message()


def test_message_list_initialization():
    """
    Test the initialization of a MessageList object.


    """
    assert MessageList() == MessageList(__root__=[])


def test_message_list_get_message():
    """
    Test the get method of the MessageList object.


    """
    message_list = MessageList()
    message_list.add_message("example")
    assert message_list.get_messages() == [{"message": "example"}]

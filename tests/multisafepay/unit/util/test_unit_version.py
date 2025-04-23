# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.util.version import Version


def test_version_initialization():
    """
    Test the initialization of a Version object with specific plugin and SDK versions.


    """
    version = Version(plugin_version="1.0.1")
    assert version.plugin_version == "1.0.1"


def test_version_deserialization():
    """
    Test the deserialization of a Version object to a dictionary.


    """
    version = Version(plugin_version="1.0.1")
    assert version.dict() == {"plugin_version": "1.0.1"}


def test_version_serialization():
    """
    Test the serialization of a Version object to a JSON string.


    """
    version = Version(plugin_version="1.0.1")
    assert version.json() == '{"plugin_version": "1.0.1"}'


def test_empty_version_initialization():
    """
    Test the initialization of a Version object without providing any version values.


    """
    version = Version()
    assert version.plugin_version == "unknown"


def test_empty_version_deserialization():
    """
    Test the deserialization of an empty Version object to a dictionary.

    """
    version = Version()
    assert version.dict() == {"plugin_version": "unknown"}


def test_empty_version_serialization():
    """
    Test the serialization of an empty Version object to a JSON string.

    """
    version = Version()
    assert version.json() == '{"plugin_version": "unknown"}'


def test_version_get_plugin_version():
    """
    Test the get_plugin_version method of the Version object.


    """
    version = Version(plugin_version="1.0.1")
    assert version.get_plugin_version() == "1.0.1"


def test_version_get_version():
    """
    Test the get_version method of the Version object.

    """
    version = Version(plugin_version="1.0.1")
    print(version.get_version())
    assert version.get_version() == "Plugin 1.0.1"


def test_version_set_plugin_version():
    """
    Test the set_plugin_version method of the Version object.


    """
    version = Version()
    version.set_plugin_version("1.0.1")
    assert version.plugin_version == "1.0.1"

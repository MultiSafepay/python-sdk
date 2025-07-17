# Changelog

All notable changes to the MultiSafepay Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2025-07-17

## Added
- PTHMINT-75: Remove unsupported attribute in delivery object (#26)
- PTHMINT-74: Encode dinamic path segment (#25)
- PTHMINT-72: Fix dependabot report (#22)
- PTHMINT-50: Fix ruff B904
- PTHMINT-49: Fix ruff B006
- PTHMINT-48: Fix ruff ARG002 
- PTHMINT-47: Fix ruff ANN401
- PTHMINT-46: Fix ruff ANN204
- PTHMINT-45: Fix ruff error code ANN201
- PTHMINT-44: Remove code ANN102 from ruff ignore
- PTHMINT-42: Fix ruff error ANN101 occurrences
- PTHMINT-41: Fix error ANN003 occurences
- PTHMINT-38: Fix ruff problems code ANN001
- PTHMINT-37: Remove A002 code to ruff lint (#11)

## [1.0.1] - 2025-04-23

### Added
- PTHMINT-66: Release of 1.0.0 - Stable version

## [1.0.0rc3] - 2025-04-23

### Removed
- PTHMINT-64: Remove sdk version property from Plugin object

## [1.0.0rc2] - 2025-04-23

### Added
- PTHMINT-59: Add readme, repository, and homepage missing properties in pyproject.toml

## [1.0.0rc1] - 2025-04-21

### Added
- Initial release candidate
- Core API functionality
- Support for payment methods
- Order creation and management
- Transaction handling
- Webhook support
- Comprehensive test suite
- Type hints and documentation
- Dependencies:
  - Python >=3.8,<3.14
  - requests ^2.32.3
  - toml ^0.10.2
  - pydantic ^1.10.0
  - python-dotenv ^1.0.1
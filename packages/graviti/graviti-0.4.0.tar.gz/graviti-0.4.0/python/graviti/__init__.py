#!/usr/bin/env python3
#
# Copyright 2021 Graviti. All Rights Reserved.
#

"""Graviti python SDK."""

import warnings

DEPRECATION_MESSAGE = """
##########################################################################
This package is deprecated, please use 'tensorbay' instead.

- Install tensorbay package:
$ pip3 install tensorbay

- Start using tensorbay:
>>> from tensorbay import GAS

Reference:
- Github: https://github.com/Graviti-AI/tensorbay-python-sdk
- Pypi: https://pypi.org/project/tensorbay/
- Documentation: https://tensorbay-python-sdk.graviti.com/en/stable/
##########################################################################
"""

with warnings.catch_warnings():
    warnings.simplefilter("always")
    warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning)


__version__ = "0.4.0"

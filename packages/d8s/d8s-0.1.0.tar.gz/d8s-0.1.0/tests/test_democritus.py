#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `democritus` module."""

import pytest

from democritus import democritus


@pytest.fixture
def response():
    return "foo bar"


def test_democritus_initialization():
    assert 1 == 1

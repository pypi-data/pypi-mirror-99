#!/usr/bin/env python
# coding: utf-8
import os
import sys
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from dbio.util.fs_helper import FSHelper
from unittest import mock


class TestFSHelper(unittest.TestCase):

    def test_get_days_since_last_modified(self):
        file = "file"
        with mock.patch('os.path.getmtime') as mock_getmtime:
            FSHelper.get_days_since_last_modified(file)
            self.assertTrue(mock_getmtime.calledWith(file))


if __name__ == "__main__":
    unittest.main()

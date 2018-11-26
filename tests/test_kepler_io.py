#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `kepler.io` submodule"""
import unittest
from unittest.mock import patch

from kepler import io


class ResponseMock:
    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text

class MAST_UnitTest(unittest.TestCase):
    """Performs unittest on the kepler MAST interface"""

    def test_id_formatting(self):
        ref_id = 1
        expected = '000000001'
        self.assertEqual(io.MAST.format_id(ref_id), expected)

    def test_against_large_id(self):
        ref_id = 1111111111  # 10 Digit ID
        with self.assertRaises(ValueError):
            io.MAST.format_id(ref_id)

    def test_against_non_integer_id(self):
        ref_id = 'Definitely not an integer.'
        with self.assertRaises(ValueError):
            io.MAST.format_id(ref_id)

    @patch('requests.get')
    def test_extract_id(self, get):
        get.return_value = ResponseMock(status_code=200, text='href="success.tar"')
        ref_id = 1
        formatted_id = io.MAST.format_id(ref_id)
        tar_url = io.MAST.get_lightcurve_tar_url(ref_id)
        self.assertIn(
            f'{formatted_id[:4]}/{formatted_id}/success.tar',
            tar_url
        )

    @patch('requests.get')
    def test_no_tarfile(self, get):
        get.return_value = ResponseMock(status_code=200, text='no tar file')
        with self.assertRaises(io.exceptions.MAST_IDNotFound):
            io.MAST.get_lightcurve_tar_url(10)

    @patch('requests.get')
    def test_400_error(self, get):
        get.return_value = ResponseMock(status_code=400)
        with self.assertRaises(io.exceptions.MAST_IDNotFound):
            io.MAST.get_lightcurve_tar_url(10)

    @patch('requests.get')
    def test_500_error(self, get):
        get.return_value = ResponseMock(status_code=500)
        with self.assertRaises(io.exceptions.MAST_ServerError):
            io.MAST.get_lightcurve_tar_url(10)

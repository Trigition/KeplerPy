import unittest
import tarfile
import os
from unittest.mock import patch
import tempfile
from kepler.io import DataCache

class TarMock:
    """ Wraps a tarfile object for mocking """
    def __init__(self, name):
        self.name = name


class Cache_UnitTests(unittest.TestCase):
    """ Performs unit tests on the DataCache class."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = self.temp.name

    def test_load_cache(self):
        basic_config = open(f'{self.directory}{os.sep}kepler_data.cache', 'wt')
        basic_tar = tarfile.open(
            fileobj=tempfile.NamedTemporaryFile(),
            mode='w'
        )
        basic_tar.add(basic_config.name)
        basic_tar.close()
        id_ref = 100
        path_ref = basic_tar.name
        basic_config.write(f'{id_ref}: "{path_ref}"\n')
        basic_config.close()
        test_cache = DataCache(self.directory)

        self.assertTrue(len(test_cache.keys()), 1)
        self.assertTrue(id_ref in test_cache.data_paths)
        self.assertEqual(test_cache[id_ref].name, path_ref)

    def test_empty_directory(self):
        new_dir = 'staticdirectory'
        target_dir = f'{self.directory}{os.sep}{new_dir}'
        self.assertFalse(os.path.exists(target_dir))
        test_cache = DataCache(target_dir)

        self.assertTrue(os.path.exists(target_dir))
        self.assertEqual(len(test_cache.keys()), 0)

    @patch('kepler.io.cache.download_lightcurve_for')
    def test_MAST_contact(self, mock):
        test_cache = DataCache(self.directory)
        mock.return_value(TarMock('tarbytes'))

        self.assertEqual(len(test_cache.keys()), 0)

        val = test_cache[100]

        self.assertTrue(mock.called)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import tarfile

if os.name == 'nt':
    from .MAST import download_lightcurve_for
    from .exceptions import MangledCache
else:
    from kepler.io.MAST import download_lightcurve_for
    from kepler.io.exceptions import MangledCache

CACHENAME = 'kepler_data.cache'


class DataCache:

    """ This class encapsulates a cache of Kepler Data """
    def __init__(self, path):
        """ Attempts to construct a cache at the given location. If the
        location is empty/has no cache, one will be created.
        :path: The path to attempt to construct a cache from.
        """
        self.data_paths = {}
        self.path = path
        self.config_filepath = f'{path}{os.sep}{CACHENAME}'
        try:
            self.load_config()
        except FileNotFoundError:
            print('No config found, creating one...')
            os.makedirs(path, exist_ok=True)
            self.write_config()
        except NotADirectoryError:
            print('Cache directory not found, attempting to make path...')
            os.makedirs(path, exist_ok=True)
            self.write_config()

    def __getitem__(self, key):
        """ Attempt to get data from cache.

        Note: The act of accessing by a key returns a new file descriptor for
        the tar object.

        """
        if key not in self.data_paths:
            # Attempt to download from MAST
            tar = download_lightcurve_for(key, self.path)
            self.data_paths[key] = tar.name
            self.write_config()
            return tarfile.open(fileobj=tar, mode='r')
        return tarfile.open(name=self.data_paths[key])


    def keys(self):
        return self.data_paths.keys()

    def write_config(self):
        with open(self.config_filepath, 'wt') as f:
            for kepler_id, path in self.data_paths.items():
                f.write(f'{kepler_id}: "{path}"\n')

    def load_config(self):
        extractor = re.compile(r'([0-9]+): \"([^\"]+)\"')
        with open(self.config_filepath, 'rt') as f:
            line_no = 0
            lines = f.readlines()
            try:
                for line in lines:
                    kepler_id, path = extractor.search(line).groups()
                    kepler_id = int(kepler_id)
                    path = path.strip()

                    self.data_paths[kepler_id] = path
                    line_no += 1
            except ValueError:
                raise MangledCache(lines[line_no], line_no)

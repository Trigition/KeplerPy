# -*- coding: utf-8 -*-
import requests
import exceptions
import re
import os
import tempfile
import tarfile
import pandas as pd
from astropy.table import Table
from io import BytesIO


MAST_BASE_URL = 'https://archive.stsci.edu/pub/kepler/lightcurves/'


def format_id(kepler_id):
    """Formats the id to be a zero padded integer with a length of 9 characters.
    No ID is greater than 9 digits and this function will throw a ValueError
    if such an integer is given.
    :kepler_id: The Kepler ID as an integer.
    :returns: A 0 padded formatted string of length 9.
    """
    return f'{kepler_id:09d}'


def get_lightcurve_tar_url(kepler_id):
    """Finds the bundled lightcurve TAR file for the given Kepler ID.

    :kepler_id: The unique kepler ID to search data for.
    :returns: The response from MAST.

    """
    id_str = format_id(kepler_id)
    url = MAST_BASE_URL + f'{id_str[:4]}/{id_str}/'

    response = requests.get(url)
    if 500 <= response.status_code:
        raise exceptions.MAST_ServerError(url, response.status_code)
    elif 400 <= response.status_code < 500:
        raise exceptions.MAST_IDNotFound(kepler_id)

    tar_url = re.search(r'href=\"(\w+\.tar)\"', response.text)
    if tar_url is None:
        raise exceptions.MAST_IDNotFound(kepler_id)

    return url + tar_url.groups()[0]


def download_lightcurve_for(kepler_id, path=None):
    """Downloads lightcurve data for the given Kepler ID.
    :kepler_id: The unique Kepler ID to download data for.
    :path: The path to place data in. If None is given the data will be placed
    in memory.
    :returns: If a specified path was given, a File Descriptor will be returned
    otherwise the data will be returned as a bytearray.
    """
    url = get_lightcurve_tar_url(kepler_id)
    if path:
        filename = f'{path}{os.sep}{kepler_id}-lightcurves.tar'
        stream = requests.get(url, stream=True)
        f = open(filename, 'wb')
        for chunk in stream.iter_content(chunk_size=2048):
            if chunk:
                f.write(chunk)
        f.seek(0)
        return f
    else:
        stream = requests.get(url, stream=True)
        chunks = [chunk for chunk in stream.iter_content(chunk_size=2048) if chunk]
        return b''.join(chunks)


def decompress_tar_bundle(tarbytes):
    filelike = BytesIO(tarbytes)
    tar = tarfile.open(fileobj=filelike)
    return [tar.extractfile(member) for member in tar.getmembers()]


def get_dataframe(kepler_id):
    raw_tarbytes = download_lightcurve_for(kepler_id)
    files = decompress_tar_bundle(raw_tarbytes)
    tables = [Table.read(f, format='fits') for f in files]
    dfs = [table.to_pandas() for table in tables]
    return pd.concat(dfs)

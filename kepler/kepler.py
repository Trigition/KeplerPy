# -*- coding: utf-8 -*-

"""Main module."""
from kepler.io.cache import DataCache
from kepler.io.lightcurve import tar_to_lightcurves, combine_curves
from kepler.processing.fits import get_fits_from_tar, normalize_series
from astropy.table import Table
import pandas as pd

class Kepler:

    def __init__(self, cache_dir='cache'):
        self.cache = DataCache(cache_dir)

    def get_fits(self, key):
        tar = self.cache[key]
        fits = get_fits_from_tar(tar)
        tar.close()
        return fits

    def get_lightcurves(self, key, curvetype='PDCSAP_FLUX'):
        tar = self.cache[key]
        lightcurves = tar_to_lightcurves(tar)
        return lightcurves

    def get_combined_lightcurve(self, key, curvetype='PDCSAP_FLUX'):
        curves = self.get_lightcurves(key, curvetype=curvetype)
        return combine_curves(curves)


    def get_dataframe(self, key, normalize=True, fields=['PDCSAP_FLUX']):
        fits = self.get_fits(key)
        tables = [Table.read(f[1]) for f in fits]
        dfs = [t.to_pandas() for t in tables]
        if normalize:
            for df in dfs:
                for field in fields:
                    df[field] = normalize_series(df[field])
        return pd.concat(dfs)

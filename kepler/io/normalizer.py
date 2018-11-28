#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This module defines various normalizing methods for various stages in the
kepler pipeline.
"""


def equalize_fits(*fits_files):
    raise NotImplementedError


def determine_julian_date(cadence_number, orbital_attributes):
    raise NotImplementedError


def dft(df, columns):
    for column in columns:
        # df[f'{column}-fft'] = fft(df[column])
        raise NotImplementedError

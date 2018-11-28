# -*- coding: utf-8 -*-

""" Loads static KIC data for easy referencing """

import os

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(), os.path.dirname(__file__)
    )
)

def load_ids(filepath):
    return [s.strip() for s in open(filepath, 'rt').readlines()]

all_kic_path = os.path.join(__location__, 'kepler_ids.txt')
kic_with_transit_path = os.path.join(__location__, 'transit_kic.txt')

all_kic = load_ids(all_kic_path)
kic_with_transit = load_ids(kic_with_transit_path)

__all__ = ['all_kic', 'kic_with_transit']

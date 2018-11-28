# -*- coding: utf-8 -*-

from tempfile import gettempdir
from lightkurve.search import open as open_lightcurve
import os


def tar_to_lightcurves(tar_fd, curvetype='PDCSAP_FLUX'):
    tempdir = gettempdir()
    lightcurves = []
    members = tar_fd.getmembers()
    for member in members:
        tar_fd.extract(member, path=tempdir)
        path = f'{tempdir}{os.sep}{member.name}'
        lightcurves.append(open_lightcurve(path).get_lightcurve(curvetype))
    return lightcurves


def combine_curves(curves):
    head = curves[0].normalize().flatten()
    return head.append([x.normalize().flatten() for x in curves[1:]])

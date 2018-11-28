from astropy.io import fits


def get_fits_from_tar(tar_fd):
    members = tar_fd.getmembers()
    return [fits.open(tar_fd.extractfile(member)) for member in members]


def convert_to_julian_dates(df, startdate):
    pass


def normalize_series(series):
    return (series - series.mean()) / (series.max() - series.min())


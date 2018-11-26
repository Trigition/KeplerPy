from astropy.io import fits


def get_fits_from_tar(tar_fd):
    members = tar_fd.members()
    return [fits.open(tar_fd.extractfile(member) for member in members]

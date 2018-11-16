class KeplerIOError(Exception):

    """A base exception for any IO error that might occur."""

    def __init__(self, message):
        """Initializes a new KeplerIOError"""
        super().__init__(message)


class MAST_IDNotFound(KeplerIOError):

    """The searched ID could not be found on MAST."""

    def __init__(self, kepler_id):
        super().__init__(f'Could not find lightcurve data for {kepler_id}.')


class MAST_ServerError(KeplerIOError):

    """Raised when the MAST server replies with a 500 error code"""
    def __init__(self, url, error):
        if error == 503:
            message = (
                f'Requesting {url} from MAST resulted in 503 Error. '
                'Please wait for service to resume or contact MAST '
                'support for more information.'
            )
        elif error == 504:
            message = (
                f'Connection to MAST resulted in 504 Gateway Timeout error. '
                'Please check connection if you\'re using a proxy or some '
                'other form of indirect connection to MAST.'
            )
        else:
            message = (
                f'MAST Service error {error} while requesting {url}. Please '
                'wait and try again.'
            )
        super().__init__(message)

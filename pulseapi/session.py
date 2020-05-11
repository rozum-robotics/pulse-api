import enum
import contextlib
import functools

import pdhttp
import pulseapi
# Session token expired

class Session:
    READ_WRITE = pdhttp.Session(mode="READ_WRITE")
    READ_ONLY = pdhttp.Session(mode="READ_ONLY")

    def __init__(self, location: str):
        self._api = pdhttp.SessionApi()
        self._api.api_client.configuration.host = location
        self._token = None
        self.location = location

    def open_session(self, mode: pdhttp.Session):
        self._mode = mode
        _, _, headers = self._api.open_session_with_http_info(
            self._mode, _return_http_data_only=False
        )
        self._token = headers["Authentication-Info"]

    def close_session(self):
        if self._token is not None:
            self._api.delete_session(self._token)
            self._token = None
        self._mode = None

    def __enter__(self):
        self.open_session(self.READ_WRITE)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_session()
        if exc_value is not None:
            raise exc_value
        
    @property
    def token(self):
        return self._token

    @property
    def mode(self):
        return self._mode

    @property
    def location(self):
        return self._api.api_client.configuration.host
    
    @location.setter
    def location(self, new_location):
        self._api.api_client.configuration.host = new_location
    
    @contextlib.contextmanager
    def read_only(self):
        try:
            self.open_session(self.READ_ONLY)
            yield self
        except:
            raise
        finally:
            self.close_session()


def refresh_token(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        obj = args[0]
        try:
            result = func(*args, **kwargs)
        except pulseapi.PulseApiException as pae:
            if "expired" in pae.body:
                session = obj._session
                session.open_session(session.mode)
                result = func(*args, **kwargs)
        return result
    
    return wrapper

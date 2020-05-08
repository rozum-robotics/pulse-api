import enum
import pdhttp


class Session:
    READ_WRITE = pdhttp.Session(mode="READ_WRITE")
    READ_ONLY = pdhttp.Session(mode="READ_ONLY")

    def __init__(self, location: str):
        self._api = pdhttp.SessionApi()
        self._api.api_client.configuration.host = location
        self._token = None

    def open_session(self, mode: pdhttp.Session):
        _, _, headers = self._api.open_session_with_http_info(
            mode, _return_http_data_only=False
        )
        self._token = headers["Authentication-Info"]

    def close_session(self):
        if self._token is None:
            raise AttributeError(
                "The session token is None. Check that you openned sesion first."
            )
        self._api.delete_session(self._token)
        self._token = None

    @property
    def token(self):
        return self._token

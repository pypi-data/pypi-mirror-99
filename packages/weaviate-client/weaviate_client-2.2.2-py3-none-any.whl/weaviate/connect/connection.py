import datetime
import time
from typing import Tuple, Optional
import requests
from requests import RequestException
from weaviate.exceptions import AuthenticationFailedException
from weaviate.connect.constants import *
from weaviate.auth import AuthCredentials
from weaviate.util import _get_valid_timeout_config


class Connection:
    """
    Connection class used to communicate to a weaviate instance.
    """
    def __init__(self,
            url: str,
            auth_client_secret: Optional[AuthCredentials]=None,
            timeout_config: Optional[Tuple[int, int]]=None
        ):
        """
        Initialize a Connection class instance.

        Parameters
        ----------
        url : str
            URL to a running weaviate instance.
        auth_client_secret : weaviate.auth.AuthCredentials, optional
            User login credentials to a weaviate instance, by default None
        timeout_config : tuple(int, int), optional
            Set the timeout config as a tuple of (retries, time out seconds),
            by default None.
        """

        self.url = url + WEAVIATE_REST_API_VERSION_PATH  # e.g. http://localhost:80/v1
        if timeout_config is None:
            self._timeout_config = (2, 20)
        else:
            self.timeout_config = timeout_config # this uses the setter

        self.auth_expires = 0  # unix time when auth expires
        self.auth_bearer = 0
        self.auth_client_secret = auth_client_secret

        self.is_authentication_required = False
        try:
            request = requests.get(
                self.url + "/.well-known/openid-configuration",
                headers={"content-type": "application/json"},
                timeout=(30, 45)
                )
        except Exception:
            pass
        else:
            if request.status_code == 200:
                if isinstance(auth_client_secret, AuthCredentials):
                    self.is_authentication_required = True
                    self._refresh_authentication()
                else:
                    raise ValueError("No login credentials provided. The weaviate instance at "
                        f"{url} requires login credential, use argument 'auth_client_secret'.")

    # Requests a new bearer
    def _refresh_authentication(self) -> None:
        """
        Request a new bearer.

        Raises
        ------
        AuthenticationFailedException
            If cannot connect to weaviate.
        AuthenticationFailedException
            If cannot authenticate http status not ok.
        AuthenticationFailedException
            If cannot connect to the third party authentication service.
        AuthenticationFailedException
            If status not OK in connection to the third party authentication service.
        AuthenticationFailedException
            If the grant_types supported by the thirdparty authentication service are insufficient.
        AuthenticationFailedException
            If unable to get a OAuth token from server.
        AuthenticationFailedException
            If authtentication access denied.
        """

        if self.auth_expires < get_epoch_time():
            # collect data for the request
            try:
                request = requests.get(
                    self.url + "/.well-known/openid-configuration",
                    headers={"content-type": "application/json"},
                    timeout=(30, 45)
                    )
            except RequestException as error:
                raise AuthenticationFailedException("Cannot connect to weaviate.") from error
            if request.status_code != 200:
                raise AuthenticationFailedException("Cannot authenticate http status not ok.")

            # Set the client ID
            client_id = request.json()['clientId']

            self._set_bearer(client_id=client_id, href=request.json()['href'])

    def _set_bearer(self, client_id: str, href: str) -> None:
        """
        Set bearer for a refreshed authentication.

        Parameters
        ----------
        client_id : str
            The client ID of the OpenID Connect.
        href : str
            The URL of the OpenID Connect issuer.

        Raises
        ------
        AuthenticationFailedException
            If authentication failed.
        """

        # request additional information
        try:
            request_third_part = requests.get(
                href,
                headers={"content-type": "application/json"},
                timeout=(30, 45)
                )
        except RequestException as error:
            raise AuthenticationFailedException(
                "Can't connect to the third party authentication service. "
                "Check that it is running.") from error
        if request_third_part.status_code != 200:
            raise AuthenticationFailedException(
                "Status not OK in connection to the third party authentication service.")

        # Validate third part auth info
        if 'client_credentials' not in request_third_part.json()['grant_types_supported']:
            raise AuthenticationFailedException(
                "The grant_types supported by the thirdparty authentication service are "
                "insufficient. Please add 'client_credentials'.")

        request_body = self.auth_client_secret.get_credentials()
        request_body["client_id"] = client_id

        # try the request
        try:
            request = requests.post(
                request_third_part.json()['token_endpoint'],
                request_body,
                timeout=(30, 45)
                )
        except RequestException:
            raise AuthenticationFailedException(
                "Unable to get a OAuth token from server. Are the credentials "
                "and URLs correct?") from None

        # sleep to process
        time.sleep(0.125)

        if request.status_code == 401:
            raise AuthenticationFailedException(
                "Authtentication access denied. Are the credentials correct?"
            )
        self.auth_bearer = request.json()['access_token']
        # -2 for some lagtime
        self.auth_expires = int(get_epoch_time() + request.json()['expires_in'] - 2)

    def _get_request_header(self) -> dict:
        """
        Returns the correct headers for a request.

        Returns
        -------
        dict
            Request header as a dict.
        """

        header = {"content-type": "application/json"}

        if self.is_authentication_required:
            self._refresh_authentication()
            header["Authorization"] = "Bearer " + self.auth_bearer

        return header

    def run_rest(self,
            path: str,
            rest_method: int,
            weaviate_object: dict=None,
            params: dict=None
        ) -> requests.Response:
        """
        Make a request to the weaviate instance.

        Parameters
        ----------
        path : str
            Sub-path to the weaviate resources. Must be a valid weaviate sub-path.
            e.g. /meta or /objects, without version.
        rest_method : int
            Type of the rest API request. Is defined through a constant given in
            the package e.g. REST_METHOD_GET.
        weaviate_object : dict, optional
            Object is used as payload, by default None
        params : dict, optional
            Additional request prameters, by default None

        Returns
        -------
        requests.Response
            The response if request was successful.

        Raises
        ------
        requests.exceptions.ConnectionError
            If the request could not be made.
            (from requests.'method' calls)
        """

        if params is None:
            params = {}
        request_url = self.url+path

        if rest_method == REST_METHOD_GET:
            response = requests.get(
                url=request_url,
                headers=self._get_request_header(),
                timeout=self._timeout_config,
                params=params
                )
        elif rest_method == REST_METHOD_PUT:
            response = requests.put(
                url=request_url,
                json=weaviate_object,
                headers=self._get_request_header(),
                timeout=self._timeout_config
                )
        elif rest_method == REST_METHOD_POST:
            response = requests.post(
                url=request_url,
                json=weaviate_object,
                headers=self._get_request_header(),
                timeout=self._timeout_config
                )
        elif rest_method == REST_METHOD_PATCH:
            response = requests.patch(
                url=request_url,
                json=weaviate_object,
                headers=self._get_request_header(),
                timeout=self._timeout_config
                )
        elif rest_method == REST_METHOD_DELETE:
            response = requests.delete(
                url=request_url,
                json=weaviate_object,
                headers=self._get_request_header(),
                timeout=self._timeout_config
                )
        else:
            print("Not yet implemented rest method called")
            response = None
        return response

    @property
    def timeout_config(self):
        """
        Getter for the `timeout_config`.
        """

        return self._timeout_config

    @timeout_config.setter
    def timeout_config(self, timeout_config: Optional[Tuple[int, int]]):
        """
        Setter for `timeout_config`.

        Parameters
        ----------
        timeout_config : tuple(int, int) or list[int, int]
            Timeout config as a tuple/list of (retries, time out seconds).
        """

        self._timeout_config = _get_valid_timeout_config(timeout_config)

def get_epoch_time() -> int:
    """
    Get the current epoch time as an integer.

    Returns
    -------
    int
        Current epoch time.
    """

    dts = datetime.datetime.utcnow()
    return round(time.mktime(dts.timetuple()) + dts.microsecond / 1e6)

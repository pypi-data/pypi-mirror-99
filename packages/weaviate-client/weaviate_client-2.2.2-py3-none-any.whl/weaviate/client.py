from typing import Optional, Tuple
from weaviate.exceptions import UnexpectedStatusCodeException, RequestsConnectionError
from .connect import Connection, REST_METHOD_GET
from .classification import Classification
from .schema import Schema
from .contextionary import Contextionary
from .batch import Batch
from .data import DataObject
from .gql import Query
from .auth import AuthCredentials


class Client:
    """
    A python native weaviate client.
    """

    def __init__(self,
            url: str,
            auth_client_secret: AuthCredentials=None,
            timeout_config: Optional[Tuple[int, int]]=None
        ):
        """
        Initialize a Client class instance.

        Parameters
        ----------
        url : str
            The URL to the weaviate instance.
        auth_client_secret : weaviate.AuthCredentials, optional
            Authentification client secret, by default None.
        timeout_config : tuple(int, int), optional
            Set the timeout config as a tuple of (retries, time out seconds),
            by default None.

        Raises
        ------
        TypeError
            If arguments are of a wrong data type.
        """

        if not isinstance(url, str):
            raise TypeError("URL is expected to be string but is " + str(type(url)))
        if url.endswith("/"):
            # remove trailing slash
            url = url[:-1]

        self._connection = Connection(
            url=url,
            auth_client_secret=auth_client_secret,
            timeout_config=timeout_config
        )
        self.classification = Classification(self._connection)
        self.schema = Schema(self._connection)
        self.contextionary = Contextionary(self._connection)
        self.batch = Batch(self._connection)
        self.data_object = DataObject(self._connection)
        self.query = Query(self._connection)

    def is_ready(self) -> bool:
        """
        Ping weaviates ready state

        Returns
        -------
        bool
            True if weaviate is ready to accept requests,
            False otherwise.
        """

        try:
            response = self._connection.run_rest("/.well-known/ready", REST_METHOD_GET)
            if response.status_code == 200:
                return True
            return False
        except RequestsConnectionError:
            return False

    def is_live(self) -> bool:
        """
        Ping weaviates live state.

        Returns
        --------
        bool
            True if weaviate is live and should not be killed,
            False otherwise.
        """

        response = self._connection.run_rest("/.well-known/live", REST_METHOD_GET)
        if response.status_code == 200:
            return True
        return False

    def get_meta(self) -> dict:
        """
        Get the meta endpoint description of weaviate.

        Returns
        -------
        dict
            The dict describing the weaviate configuration.

        Raises
        ------
        weaviate.UnexpectedStatusCodeException
            If weaviate reports a none OK status.
        """

        response = self._connection.run_rest("/meta", REST_METHOD_GET)
        if response.status_code == 200:
            return response.json()
        raise UnexpectedStatusCodeException("Meta endpoint", response)

    def get_open_id_configuration(self) -> Optional[dict]:
        """
        Get the openid-configuration.

        Returns
        -------
        dict
            The configuration or None if not configured.

        Raises
        ------
        weaviate.UnexpectedStatusCodeException
            If weaviate reports a none OK status.
        """

        response = self._connection.run_rest("/.well-known/openid-configuration", REST_METHOD_GET)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 404:
            return None
        raise UnexpectedStatusCodeException("Meta endpoint", response)

    @property
    def timeout_config(self):
        """
        Getter for `timeout_config`.
        """

        return self._connection.timeout_config

    @timeout_config.setter
    def timeout_config(self, timeout_config: Optional[Tuple[int, int]]):
        """
        Setter for `timeout_config`.

        Parameters
        ----------
        timeout_config : tuple(int, int) or list[int, int]
            Timeout config as a tuple of (retries, time out seconds).
        """

        self._connection.timeout_config = timeout_config

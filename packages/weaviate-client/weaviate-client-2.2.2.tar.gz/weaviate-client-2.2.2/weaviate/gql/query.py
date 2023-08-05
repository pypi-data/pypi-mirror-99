"""
GraphQL query module.
"""
import sys
from typing import List, Union
from weaviate.connect import REST_METHOD_POST, Connection
from weaviate.exceptions import UnexpectedStatusCodeException, RequestsConnectionError
from .get import GetBuilder
from .aggregate import AggregateBuilder


class Query:
    """
    Query class used to make `get` and/or `aggregate` GraphQL queries.
    """

    def __init__(self, connection: Connection):
        """
        Initialize a Classification class instance.

        Parameters
        ----------
        connection : weaviate.connect.Connection
            Connection object to an active and running weaviate instance.
        """

        self._connection = connection

    def get(self,
            class_name: str,
            properties: Union[List[str], str]
        ) -> GetBuilder:
        """
        Instantiate a GetBuilder for GraphQL `get` requests.

        Parameters
        ----------
        class_name : str
            Class name of the objects to interact with.
        properties : list of str or str
            Properties of the objetcs to interact with.

        Returns
        -------
        GetBuilder
            A GetBuilder to make GraphQL `get` requests from weaviate.
        """

        return GetBuilder(class_name, properties, self._connection)

    def aggregate(self, class_name: str) -> AggregateBuilder:
        """
        Instantiate an AggregateBuilder for GraphQL `aggregate` requests.

        Parameters
        ----------
        class_name : str
            Class name of the objects to be aggregated.

        Returns
        -------
        AggregateBuilder
            An AggregateBuilder to make GraphQL `aggregate` requests from weaviate.
        """

        return AggregateBuilder(class_name, self._connection)

    def raw(self, gql_query: str) -> dict:
        """
        Allows to send simple graph QL string queries.
        Be cautious of injection risks when generating query strings.

        Parameters
        ----------
        gql_query : str
            GraphQL query as a string.

        Returns
        -------
        dict
            Data response of the query.

        Raises
        ------
        TypeError
            If 'gql_query' is not of type str.
        requests.exceptions.ConnectionError
            If the network connection to weaviate fails.
        weaviate.UnexpectedStatusCodeException
            If weaviate reports a none OK status.
        """

        if not isinstance(gql_query, str):
            raise TypeError("Query is expected to be a string")

        json_query = {"query": gql_query}

        try:
            response = self._connection.run_rest("/graphql", REST_METHOD_POST, json_query)
        except RequestsConnectionError as conn_err:
            message = str(conn_err) + ' Connection error, query not executed.'
            raise type(conn_err)(message).with_traceback(sys.exc_info()[2])

        if response.status_code == 200:
            return response.json()  # Successfully queried
        raise UnexpectedStatusCodeException("GQL query failed", response)

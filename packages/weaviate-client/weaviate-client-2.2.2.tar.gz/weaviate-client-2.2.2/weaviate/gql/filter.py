"""
GraphQL filters for `Get` and `Aggregate` commands.
GraphQL abstract class for GraphQL commands to inherit from.
"""
import json
import sys
from copy import deepcopy
from typing import Optional
from abc import ABC, abstractmethod
from weaviate.connect import REST_METHOD_POST, Connection
from weaviate.exceptions import UnexpectedStatusCodeException, RequestsConnectionError

class GraphQL(ABC):
    """
    A base abstract class for GraphQL commands, such as Get, Aggregate.
    """

    def __init__(self, connection: Connection):
        """
        Initialize a GraphQL abstract class instance.

        Parameters
        ----------
        connection : weaviate.connect.Connection
            Connection object to an active and running weaviate instance.
        """

        self._connection = connection

    @abstractmethod
    def build(self) -> str:
        """
        Build method to be overloaded by the child classes. It should return the
        GraphQL query as a str.

        Returns
        -------
        str
            The query.
        """

    def do(self) -> dict:
        """
        Builds and runs the query.

        Returns
        -------
        dict
            The response of the query.

        Raises
        ------
        requests.exceptions.ConnectionError
            If the network connection to weaviate fails.
        weaviate.UnexpectedStatusCodeException
            If weaviate reports a none OK status.
        """

        query = self.build()

        try:
            response = self._connection.run_rest("/graphql", REST_METHOD_POST, {"query": query})
        except RequestsConnectionError as conn_err:
            message = str(conn_err) + ' Connection error, query was not successful.'
            raise type(conn_err)(message).with_traceback(sys.exc_info()[2])
        if response.status_code == 200:
            return response.json()  # success
        raise UnexpectedStatusCodeException("Query was not successful", response)


class Near(ABC):
    """
    A base abstract class for `near` filters, such as `nearText`, `nearVector` or `nearObject`.
    """

    @abstractmethod
    def __str__(self) -> str:
        """
        Should be implemented in each inheriting class.
        """


class NearText(Near):
    """
    NearText class used to filter weaviate objects.
    """

    def __init__(self, content: dict):
        """
        Initialize a NearText class instance.

        Parameters
        ----------
        content : dict
            The content of the `nearText` clause.

        Raises
        ------
        TypeError
            If 'content' is not of type dict.
        TypeError
            If 'content'  has key "certainty" but the value is not float.
        """

        if not isinstance(content, dict):
            raise TypeError(f"{self.__class__.__name__} filter is expected to "
                f"be type dict but was {type(content)}")
        _content = deepcopy(content)
        _check_concept(_content)
        self.concepts = _content["concepts"]
        self.certainty: Optional[float] = None
        self.move_to: Optional[dict] = None
        self.move_away_from: Optional[dict] = None

        if "certainty" in _content:
            _check_certainty_type(_content["certainty"])
            self.certainty = _content["certainty"]

        if "moveTo" in _content:
            _check_direction_clause(_content["moveTo"])
            self.move_to = _content["moveTo"]

        if "moveAwayFrom" in _content:
            _check_direction_clause(_content["moveAwayFrom"])
            self.move_away_from = _content["moveAwayFrom"]

    def __str__(self):
        near_text = f'nearText: {{concepts: {json.dumps(self.concepts)}'
        if self.certainty is not None:
            near_text += f' certainty: {str(self.certainty)}'
        if self.move_to is not None:
            near_text += (
                f' moveTo: {{concepts: {json.dumps(self.move_to["concepts"])} ' +\
                f'force: {self.move_to["force"]}}}'
            )
        if self.move_away_from is not None:
            near_text += (
                f' moveAwayFrom: {{concepts: {json.dumps(self.move_away_from["concepts"])} ' +\
                        f'force: {self.move_away_from["force"]}}}'
            )
        return near_text + '} '


class NearVector(Near):
    """
    NearVector class used to filter weaviate objects.
    """

    def __init__(self, content: dict):
        """
        Initialize a NearVector class instance.

        Parameters
        ----------
        content : list
            The content of the `nearVector` clause.

        Raises
        ------
        TypeError
            If 'content' is not of type dict.
        ValueError
            If 'content' does not contain "vector".
        TypeError
            If 'content["vector"]' is not of type list.
        AttributeError
            If invalid 'content' keys are provided.
        """

        if not isinstance(content, dict):
            raise TypeError(f"{self.__class__.__name__} filter is expected to "
                f"be type dict but was {type(content)}")

        _content = deepcopy(content)
        _check_vector(_content)
        self.vector = _content['vector']
        self.certainty: Optional[float] = None

        # Check optional fields

        if "certainty" in _content:
            _check_certainty_type(_content["certainty"])
            self.certainty = _content["certainty"]

    def __str__(self):
        near_vector = f'nearVector: {{vector: {json.dumps(self.vector)}'
        if self.certainty is not None:
            near_vector += f' certainty: {self.certainty}'
        return near_vector + '} '


class NearObject(Near):
    """
    NearObject class used to filter weaviate objects.
    """

    def __init__(self, content: dict):
        """
        Initialize a NearVector class instance.

        Parameters
        ----------
        content : list
            The content of the `nearVector` clause.

        Raises
        ------
        TypeError
            If 'content' is not of type dict.
        TypeError
            If 'content'  has key "certainty" but the value is not float.
        """

        if not isinstance(content, dict):
            raise TypeError(f"{self.__class__.__name__} filter is expected to "
                f"be type dict but was {type(content)}")

        if ('id' in content) == ('beacon' in content):
            raise ValueError("The 'content' argument should contain EITHER `id` OR `beacon`!")

        if 'id' in content:
            self.obj_id = 'id'
        else:
            self.obj_id = 'beacon'

        if not isinstance(content[self.obj_id], str):
            raise TypeError("The 'id'/'beacon' should be of type string! Given type"
                + str(type(content[self.obj_id])))

        if "certainty" in content:
            _check_certainty_type(content["certainty"])

        self._content = deepcopy(content)

    def __str__(self):

        near_object = f'nearObject: {{{self.obj_id}: {self._content[self.obj_id]}'
        if 'certainty' in self._content:
            near_object += f' certainty: {self._content["certainty"]}'
        return near_object + '} '


class WhereFilter:
    """
    WhereFilter class used to filter weaviate objects.
    """

    def __init__(self, content: dict):
        """
        Initialize a WhereFilter class instance.

        Parameters
        ----------
        content : dict
            The content of the `where` filter clause.

        Raises
        ------
        TypeError
            If 'content' is not of type dict.
        ValueError
            If a mandatory key is missing in the filter content.
        """

        if not isinstance(content, dict):
            raise TypeError(f"{self.__class__.__name__} is expected to be type dict but "
                f"was {type(content)}")

        if "path" in content:
            self.is_filter = True
            self._parse_filter(content)
        elif "operands" in content:
            self.is_filter = False
            self._parse_operator(content)
        else:
            raise ValueError("Filter is missing required fileds `path` or `operands`."
                f" Given: {content}")

    def _parse_filter(self, content: dict) -> None:
        """
        Set filter fields for the WhereFilter.

        Parameters
        ----------
        content : dict
            The content of the `where` filter clause.

        Raises
        ------
        ValueError
            If 'content' is missing required fields.
        """

        if "operator" not in content:
            raise ValueError("Filter is missing required filed `operator`. "
                f"Given: {content}")

        self.path = json.dumps(content["path"])
        self.operator = content["operator"]
        self.value_type = _find_value_type(content)
        self.value = content[self.value_type]

    def _parse_operator(self, content: dict) -> None:
        """
        Set operator fields for the WhereFilter.

        Parameters
        ----------
        content : dict
            The content of the `where` filter clause.

        Raises
        ------
        ValueError
            If 'content' is missing required fields.
        """

        if "operator" not in content:
            raise ValueError("Filter is missing required filed `operator`."
                f" Given: {content}")
        _content = deepcopy(content)
        self.operator = _content["operator"]
        self.operands = []
        for operand in _content["operands"]:
            self.operands.append(WhereFilter(operand))

    def __str__(self):
        if self.is_filter:
            gql = f'where: {{path: {self.path} operator: {self.operator} {self.value_type}: '
            if self.value_type in ["valueInt", "valueNumber"]:
                gql += f'{self.value}}}'
            elif self.value_type == "valueBoolean":
                bool_value = str(self.value).lower()
                gql += f'{bool_value}}}'
            elif self.value_type == "valueGeoRange":
                geo_value = json.dumps(self.value)
                gql += f'{geo_value}}}'
            else:
                gql += f'"{self.value}"}}'
            return gql + ' '

        operands_str = []
        for operand in self.operands:
            # remove the `where: ` from the operands and the last space
            operands_str.append(str(operand)[7:-1])
        operands = ", ".join(operands_str)
        return f'where: {{operator: {self.operator} operands: [{operands}]}} '


def _check_direction_clause(direction: dict) -> dict:
    """
    Validate the direction sub clause.

    Parameters
    ----------
    direction : dict
        A sub clause of the Explore filter.

    Raises
    ------
    TypeError
        If 'direction' is not a dict.
    TypeError
        If the value of the "force" key is not float.
    ValueError
        If no "force" key in the 'direction'.
    """

    if not isinstance(direction, dict):
        raise TypeError(f"`move` clause should be dict but was {type(direction)}")

    if ('concepts' not in direction) and ('objects' not in direction):
        raise ValueError("The 'move' clause should contain `concepts` OR/AND `objects`!")

    if 'concepts' in direction:
        _check_concept(direction)
    if 'objects' in direction:
        _check_objects(direction)
    if not "force" in direction:
        raise ValueError("'move' clause needs to state a 'force'")
    if not isinstance(direction["force"], float):
        raise TypeError(f"'force' should be float but was {type(direction['force'])}")


def _check_concept(content: dict) -> None:
    """
    Validate the concept sub clause.

    Parameters
    ----------
    content : dict
        An Explore (sub) clause to check for 'concepts'.

    Raises
    ------
    ValueError
        If no "concepts" key in the 'content' dict.
    TypeError
        If the value of the  "concepts" is of wrong type.
    """

    if "concepts" not in content:
        raise ValueError("No concepts in content")

    if not isinstance(content["concepts"], (list, str)):
        raise TypeError(f"Concepts must be of type list or str, not {type(content['concepts'])}")
    if isinstance(content["concepts"], str):
        content["concepts"] = [content["concepts"]]


def _check_objects(content: dict) -> None:
    """
    Validate the `objects` sub clause of the `move` clause.

    Parameters
    ----------
    content : dict
        An Explore (sub) clause to check for 'objects'.

    Raises
    ------
    ValueError
        If no "concepts" key in the 'content' dict.
    TypeError
        If the value of the  "concepts" is of wrong type.
    """

    if not isinstance(content["objects"], (list, dict)):
        raise TypeError(f"'objects' must be of type list or dict, not {type(content['objects'])}")
    if isinstance(content["objects"], dict):
        content["objects"] = [content["objects"]]

    for obj in content["objects"]:
        if len(obj) != 1 or ('id' not in obj and 'beacon' not in obj):
            raise ValueError('Each object from the `move` clause should have ONLY `id` OR '
                '`beacon`!')


def _check_vector(content: dict) -> None:
    """
    Validate the vector of the nearVector.

    Parameters
    ----------
    content : dict
        A nearVector clause to validate.

    Raises
    ------
    ValueError
        If no "vector" key in the 'content' dict.
    TypeError
        If the value of the  "vector" is of wrong type.
    """

    if "vector" not in content:
        raise ValueError("No 'vector' key in `content` argument.")
    if not isinstance(content["vector"], list):
        raise TypeError("'vector' key is expected to be type `list` but was "
            + str(type(content['vector'])))


def _check_certainty_type(certainty: float) -> None:
    """
    Check 'certainty

    Parameters
    ----------
    certainty : float
        Certainty value to check if it is of type float.
    """

    if not isinstance(certainty, float):
        raise TypeError("certainty is expected to be a float but was "
            f"{type(certainty)}")


def _find_value_type(content: dict) -> str:
    """
    Find the correct type of the content.

    Parameters
    ----------
    content : dict
        The content for which to find the appropriate data type.

    Returns
    -------
    str
        The correct data type.

    Raises
    ------
    ValueError
        If missing required fields.
    """

    if "valueString" in content:
        to_return = "valueString"
    elif "valueText" in content:
        to_return = "valueText"
    elif "valueInt" in content:
        to_return = "valueInt"
    elif "valueNumber" in content:
        to_return = "valueNumber"
    elif "valueDate" in content:
        to_return = "valueDate"
    elif "valueBoolean" in content:
        to_return = "valueBoolean"
    elif "valueGeoRange" in content:
        to_return = "valueGeoRange"
    else:
        raise ValueError(f"Filter is missing required fileds: {content}")
    return to_return

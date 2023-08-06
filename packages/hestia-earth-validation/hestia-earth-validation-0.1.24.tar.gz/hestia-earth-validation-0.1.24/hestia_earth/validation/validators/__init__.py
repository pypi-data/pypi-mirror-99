from hestia_earth.schema import SchemaType

from hestia_earth.validation.utils import _flatten, _update_error_path
from .shared import validate_empty_fields
from .cycle import validate_cycle
from .impact_assessment import validate_impact_assessment
from .organisation import validate_organisation
from .site import validate_site


VALIDATE_TYPE = {
    SchemaType.CYCLE.value: lambda n, nodes: validate_cycle(n, nodes),
    SchemaType.IMPACTASSESSMENT.value: lambda n, nodes: validate_impact_assessment(n, nodes),
    SchemaType.ORGANISATION.value: lambda n, nodes: validate_organisation(n, nodes),
    SchemaType.SITE.value: lambda n, nodes: validate_site(n, nodes)
}


def _validate_node_type(nodes: list, ntype: str, node: dict):
    validations = VALIDATE_TYPE[ntype](node, nodes) if ntype in VALIDATE_TYPE else []
    empty_warnings = validate_empty_fields(node)
    return validations + empty_warnings


def _validate_node_children(nodes: list, node: dict):
    validations = []
    for key, value in node.items():
        if isinstance(value, list):
            validations.extend([_validate_node_child(nodes, key, value, index) for index, value in enumerate(value)])
        if isinstance(value, dict):
            validations.append(_validate_node_child(nodes, key, value))
    return _flatten(validations)


def _validate_node_child(nodes: list, key: str, value: dict, index=None):
    values = validate_node(nodes)(value)
    return list(map(lambda error: _update_error_path(error, key, index) if isinstance(error, dict) else error, values))


def validate_node(nodes: list):
    def validate(node: dict):
        """
        Validates a single Node.

        Parameters
        ----------
        node : dict
            The JSON-Node to validate.

        Returns
        -------
        List
            The list of errors/warnings for the node, which can be empty if no errors/warnings detected.
        """
        ntype = node.get('type') if isinstance(node, dict) else None
        return [] if ntype is None else list(filter(lambda v: v is not True, _flatten(
            _validate_node_type(nodes, ntype, node) + _validate_node_children(nodes, node)
        )))
    return validate

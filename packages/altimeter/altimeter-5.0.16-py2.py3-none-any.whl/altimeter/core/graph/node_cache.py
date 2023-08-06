"""A NodeCache is a simple cache for graph nodes."""
from typing import Union

from rdflib import BNode, URIRef


class NodeCache(dict):
    """A NodeCache is a simple cache for graph nodes. Unlike a standard
    dict it does not allow overwriting entries."""

    def __setitem__(self, key: str, value: Union[BNode, URIRef]) -> None:
        """Set an item in this NodeCache
            key: cache key
            value: BNode value

        Raises:
            KeyError if this key is already present.
        """
        if key in self:
            raise KeyError(f"Key already present for {key}")
        super().__setitem__(key, value)

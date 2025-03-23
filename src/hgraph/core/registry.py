from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Type

if TYPE_CHECKING:
    from hgraph.core.node import Node
    from hgraph.core.edge import Edge, Hyperedge


class SchemaRegistry:
    node_types: Dict[str, Type[Node]] = {}
    edge_types: Dict[str, Type[Edge]] = {}
    hyperedge_types: Dict[str, Type[Hyperedge]] = {}

    @classmethod
    def register_node(cls, node_type: Type[Node]):
        cls.node_types[node_type.__name__] = node_type

    @classmethod
    def register_edge(cls, edge_type: Type[Edge]):
        cls.edge_types[edge_type.__name__] = edge_type

    @classmethod
    def register_hyperedge(cls, hyperedge_type: Type[Hyperedge]):
        cls.hyperedge_types[hyperedge_type.__name__] = hyperedge_type

    @classmethod
    def load_node(cls, data: dict) -> Node:
        node_class = cls.node_types[data["type"]]
        return node_class.model_validate(data)

    @classmethod
    def load_edge(cls, data: dict) -> Edge:
        edge_class = cls.edge_types[data["type"]]
        return edge_class.model_validate(data)

    @classmethod
    def load_hyperedge(cls, data: dict) -> Hyperedge:
        edge_class = cls.hyperedge_types[data["type"]]
        return edge_class.model_validate(data)

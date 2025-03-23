from typing import Type, TypeVar, Optional, List
from uuid import UUID
from hgraph.core.node import Node
from hgraph.core.edge import Edge, Hyperedge
from hgraph.core.validator import ConstraintValidator

TNode = TypeVar("TNode", bound=Node)
TEdge = TypeVar("TEdge", bound=Edge)
THyperedge = TypeVar("THyperedge", bound=Hyperedge)


class Hypergraph:
    nodes: dict[UUID, Node] = {}
    edges: dict[UUID, Edge] = {}
    hyperedges: dict[UUID, Hyperedge] = {}

    # --- Nodes ---
    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def update_node(self, node_id: UUID, updated: Node) -> None:
        self.nodes[node_id] = updated

    def delete_node(self, node_id: UUID) -> None:
        self.nodes.pop(node_id, None)

    def get_node(self, node_id: UUID) -> Optional[Node]:
        return self.nodes.get(node_id)

    def list_nodes(self) -> List[Node]:
        return list(self.nodes.values())

    # --- Edges ---
    def add_edge(self, edge: Edge) -> None:
        validator = ConstraintValidator(self.edges, self.hyperedges)
        validator.validate_edge(edge)
        self.edges[edge.id] = edge

    def update_edge(self, edge_id: UUID, updated: Edge) -> None:
        self.edges[edge_id] = updated

    def delete_edge(self, edge_id: UUID) -> None:
        self.edges.pop(edge_id, None)

    def get_edge(self, edge_id: UUID) -> Optional[Edge]:
        return self.edges.get(edge_id)

    def list_edges(self) -> List[Edge]:
        return list(self.edges.values())

    # --- Hyperedges ---
    def add_hyperedge(self, hyperedge: Hyperedge) -> None:
        validator = ConstraintValidator(self.edges, self.hyperedges)
        validator.validate_hyperedge(hyperedge)
        self.hyperedges[hyperedge.id] = hyperedge

    def update_hyperedge(self, edge_id: UUID, updated: Hyperedge) -> None:
        self.hyperedges[edge_id] = updated

    def delete_hyperedge(self, edge_id: UUID) -> None:
        self.hyperedges.pop(edge_id, None)

    def get_hyperedge(self, edge_id: UUID) -> Optional[Hyperedge]:
        return self.hyperedges.get(edge_id)

    def list_hyperedges(self) -> List[Hyperedge]:
        return list(self.hyperedges.values())

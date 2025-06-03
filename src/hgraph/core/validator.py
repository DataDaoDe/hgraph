from hgraph.core.edge import Edge, Hyperedge
from typing import Dict
from uuid import UUID


class ConstraintViolation(Exception):
    pass


class ConstraintValidator:
    def __init__(self, edges: Dict[UUID, Edge], hyperedges: Dict[UUID, Hyperedge]):
        self.edges = edges
        self.hyperedges = hyperedges

    def validate_edge(self, new_edge: Edge):
        for edge in self.edges.values():
            # --- IRREFLEXIVE ---
            if new_edge.config.irreflexive and new_edge.source == new_edge.target:
                raise ConstraintViolation(
                    f"{new_edge.type} is irreflexive but source == target"
                )

            # --- ASYMMETRIC ---
            if new_edge.config.asymmetric:
                if self._has_edge(new_edge.type, new_edge.target, new_edge.source):
                    raise ConstraintViolation(
                        f"{new_edge.type} is asymmetric but reverse exists"
                    )

            # --- ANTISYMMETRIC ---
            if new_edge.config.antisymmetric:
                if new_edge.source != new_edge.target and self._has_edge(
                    new_edge.type, new_edge.target, new_edge.source
                ):
                    raise ConstraintViolation(
                        f"{new_edge.type} is antisymmetric but reverse exists"
                    )

            # --- FUNCTIONAL ---
            if new_edge.config.functional:
                if any(
                    e.type == new_edge.type
                    and e.source == new_edge.source
                    and e.id != new_edge.id
                    for e in self.edges.values()
                ):
                    raise ConstraintViolation(
                        f"{new_edge.type} is functional: multiple targets from same source"
                    )

            # --- INVERSE FUNCTIONAL ---
            if new_edge.config.inverse_functional:
                if any(
                    e.type == new_edge.type
                    and e.target == new_edge.target
                    and e.id != new_edge.id
                    for e in self.edges.values()
                ):
                    raise ConstraintViolation(
                        f"{new_edge.type} is inverse-functional: multiple sources to same target"
                    )
            # --- DUPLICATES ---
            if not new_edge.config.allows_duplicates:
                if any(
                    e.type == new_edge.type
                    and e.source == new_edge.source
                    and e.target == new_edge.target
                    and e.id != new_edge.id
                    for e in self.edges.values()
                ):
                    raise ConstraintViolation(
                        f"Duplicate {new_edge.type} edge between {new_edge.source} and {new_edge.target}"
                    )
        # reflexive=True and symmetric=True imply permission, not enforcement → no check needed

    def validate_hyperedge(self, new_edge: Hyperedge):
        cfg = new_edge.config

        # --- IRREFLEXIVITY/CYCLICITY ---
        if not cfg.cyclic:
            overlap = set(new_edge.sources).intersection(set(new_edge.targets))
            if overlap:
                raise ConstraintViolation(
                    f"{new_edge.type} is non-cyclic but has overlapping nodes in sources and targets: {overlap}"
                )

        if cfg.reflexive is False and new_edge.sources == new_edge.targets:
            # No exact reflexive mapping if not allowed
            raise ConstraintViolation(
                f"{new_edge.type} is not reflexive but sources == targets"
            )

        # --- DUPLICATE CHECK ---
        if not cfg.allows_duplicates:
            for edge in self.hyperedges.values():
                if (
                    edge.type == new_edge.type
                    and self._compare_node_sets(
                        edge.sources, new_edge.sources, unordered=cfg.unordered
                    )
                    and self._compare_node_sets(
                        edge.targets, new_edge.targets, unordered=cfg.unordered
                    )
                ):
                    raise ConstraintViolation(
                        f"Duplicate hyperedge of type {new_edge.type} with same sources and targets"
                    )

        # --- FUNCTIONAL ---
        if cfg.functional:
            for edge in self.hyperedges.values():
                if (
                    edge.type == new_edge.type
                    and self._compare_node_sets(
                        edge.sources, new_edge.sources, unordered=cfg.unordered
                    )
                    and edge.id != new_edge.id
                    and not self._compare_node_sets(
                        edge.targets, new_edge.targets, unordered=cfg.unordered
                    )
                ):
                    raise ConstraintViolation(
                        f"{new_edge.type} is functional but multiple target sets exist for same sources"
                    )

        # --- INVERSE FUNCTIONAL ---
        if cfg.inverse_functional:
            for edge in self.hyperedges.values():
                if (
                    edge.type == new_edge.type
                    and self._compare_node_sets(
                        edge.targets, new_edge.targets, unordered=cfg.unordered
                    )
                    and edge.id != new_edge.id
                    and not self._compare_node_sets(
                        edge.sources, new_edge.sources, unordered=cfg.unordered
                    )
                ):
                    raise ConstraintViolation(
                        f"{new_edge.type} is inverse-functional but multiple source sets exist for same targets"
                    )

    def _compare_node_sets(
        self, a: list[UUID], b: list[UUID], unordered: bool = False
    ) -> bool:
        return set(a) == set(b) if unordered else a == b

    def _has_edge(self, edge_type: str, source: UUID, target: UUID) -> bool:
        return any(
            e.type == edge_type and e.source == source and e.target == target
            for e in self.edges.values()
        )

from uuid import uuid4
from hgraph.core.node import Node
from hgraph.core.edge import Hyperedge
from hgraph.core.config import HyperedgeConfig
from hgraph.core.hypergraph import Hypergraph
from hgraph.core.validator import ConstraintViolation
from hgraph.core.utils import to_graphviz

# -----------------------------
# Academic Co-Authorship
# -----------------------------


class Researcher(Node):
    name: str
    affiliation: str


class Paper(Node):
    title: str
    year: int


class CoAuthored(Hyperedge):
    sources: list
    targets: list
    config: HyperedgeConfig = HyperedgeConfig(
        unordered=True,
        allows_duplicates=False,
        cyclic=False,
        reflexive=False,
        inverse="WrittenBy",
    )


def academic_example():
    g = Hypergraph()
    # Researchers
    alice = Researcher(name="Alice", affiliation="MIT")
    bob = Researcher(name="Bob", affiliation="Stanford")
    g.add_node(alice)
    g.add_node(bob)
    # Paper
    paper = Paper(title="On the Future of AI", year=2024)
    g.add_node(paper)
    # Hyperedge
    he = CoAuthored(sources=[alice.id, bob.id], targets=[paper.id])
    g.add_hyperedge(he)
    return g


# -----------------------------
# Run example and visualize
# -----------------------------
if __name__ == "__main__":
    g1 = academic_example()
    to_graphviz(g1, "academic_graph")

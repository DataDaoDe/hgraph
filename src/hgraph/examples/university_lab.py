# file: hgraph_examples/university_lab.py

from uuid import UUID
from hgraph.core.node import Node
from hgraph.core.edge import Hyperedge
from hgraph.core.config import HyperedgeConfig
from hgraph.core.hypergraph import Hypergraph
from hgraph.core.validator import ConstraintViolation


class Professor(Node):
    name: str


class Project(Node):
    title: str


class LeadsProject(Hyperedge):
    sources: list[UUID]  # Professors
    targets: list[UUID]  # Project(s)
    config: HyperedgeConfig = HyperedgeConfig(
        unordered=True,
        allows_duplicates=False,
        cyclic=False,
        functional=True,
        inverse_functional=True,
    )


def test_hyperedge_constraints():
    hg = Hypergraph()

    # --- Professors ---
    alice = Professor(name="Prof. Alice")
    bob = Professor(name="Prof. Bob")
    charlie = Professor(name="Prof. Charlie")

    # --- Projects ---
    ai_project = Project(title="AI Ethics")
    physics_project = Project(title="Quantum Computing")

    # Add nodes
    for node in [alice, bob, charlie, ai_project, physics_project]:
        hg.add_node(node)

    # --- Valid hyperedge ---
    edge1 = LeadsProject(sources=[alice.id, bob.id], targets=[ai_project.id])
    hg.add_hyperedge(edge1)
    print("✅ Added first LeadsProject hyperedge (Alice + Bob → AI Ethics)")

    # --- Violation of functional constraint ---
    try:
        edge2 = LeadsProject(
            sources=[alice.id, bob.id],
            targets=[physics_project.id],  # Same source team → different target
        )
        hg.add_hyperedge(edge2)
    except ConstraintViolation as e:
        print("❌ Functional constraint violation:", e)

    # --- Violation of inverse-functional constraint ---
    try:
        edge3 = LeadsProject(
            sources=[charlie.id],
            targets=[ai_project.id],  # Same project as in edge1 → different team
        )
        hg.add_hyperedge(edge3)
    except ConstraintViolation as e:
        print("❌ Inverse-functional constraint violation:", e)

    # --- Violation of cyclic = False ---
    try:
        edge4 = LeadsProject(sources=[alice.id], targets=[alice.id])
        hg.add_hyperedge(edge4)
    except ConstraintViolation as e:
        print("❌ Cyclic constraint violation:", e)


if __name__ == "__main__":
    test_hyperedge_constraints()

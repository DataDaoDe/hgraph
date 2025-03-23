from uuid import uuid4
from hgraph.core.node import Node
from hgraph.core.edge import Hyperedge
from hgraph.core.config import HyperedgeConfig
from hgraph.core.hypergraph import Hypergraph
from hgraph.core.validator import ConstraintViolation
from hgraph.core.utils import to_graphviz

# -----------------------------
# Medical Diagnosis
# -----------------------------


class Symptom(Node):
    name: str


class RiskFactor(Node):
    name: str


class Diagnosis(Node):
    name: str


class CausesDiagnosis(Hyperedge):
    sources: list
    targets: list
    config: HyperedgeConfig = HyperedgeConfig(
        unordered=False,
        allows_duplicates=False,
        cyclic=False,
        functional=False,
        inverse_functional=True,
    )


def medical_example():
    g = Hypergraph()
    fever = Symptom(name="Fever")
    cough = Symptom(name="Cough")
    smoker = RiskFactor(name="Smoker")
    pneumonia = Diagnosis(name="Pneumonia")

    for node in [fever, cough, smoker, pneumonia]:
        g.add_node(node)

    he = CausesDiagnosis(
        sources=[fever.id, cough.id, smoker.id], targets=[pneumonia.id]
    )
    g.add_hyperedge(he)
    return g


# -----------------------------
# Run example and visualize
# -----------------------------
if __name__ == "__main__":
    g1 = medical_example()
    to_graphviz(g1, "medical_graph")

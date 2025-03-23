from uuid import UUID
from hgraph.core.node import Node
from hgraph.core.edge import Edge
from hgraph.core.config import EdgeConfig
from hgraph.core.hypergraph import Hypergraph


# --- Define Models ---
class Person(Node):
    name: str
    age: int


class HasChild(Edge):
    source: UUID
    target: UUID
    config: EdgeConfig = EdgeConfig(
        antisymmetric=True, irreflexive=True, inverse="HasParent"
    )


class FatherOf(Edge):
    source: UUID
    target: UUID
    config: EdgeConfig = EdgeConfig(
        antisymmetric=True, irreflexive=True, inverse="HasFather"
    )


class MotherOf(Edge):
    source: UUID
    target: UUID
    config: EdgeConfig = EdgeConfig(
        antisymmetric=True, irreflexive=True, inverse="HasMother"
    )


class SiblingOf(Edge):
    source: UUID
    target: UUID
    config: EdgeConfig = EdgeConfig(symmetric=True, irreflexive=True)


# --- Initialize Hypergraph ---
graph = Hypergraph()

# --- Add Persons ---
james = Person(name="James Smith", age=45)
lauren = Person(name="Lauren Smith", age=43)

thomas = Person(name="Thomas Smith", age=17)
thalia = Person(name="Thalia Smith", age=15)
timothy = Person(name="Timothy Smith", age=12)
tula = Person(name="Tula Smith", age=10)

for person in [james, lauren, thomas, thalia, timothy, tula]:
    graph.add_node(person)

# --- Define Relationships ---
edges = []

# Parent relationships
for child in [thomas, thalia, timothy, tula]:
    edges.append(FatherOf(source=james.id, target=child.id))
    edges.append(MotherOf(source=lauren.id, target=child.id))
    edges.append(HasChild(source=james.id, target=child.id))
    edges.append(HasChild(source=lauren.id, target=child.id))

# Sibling relationships
siblings = [thomas, thalia, timothy, tula]
for i in range(len(siblings)):
    for j in range(i + 1, len(siblings)):
        edges.append(SiblingOf(source=siblings[i].id, target=siblings[j].id))
        edges.append(
            SiblingOf(source=siblings[j].id, target=siblings[i].id)
        )  # symmetric edge

# Add all edges
for edge in edges:
    graph.add_edge(edge)

# --- Print Output ---
print("📌 Nodes:")
for node in graph.list_nodes():
    print(f"- {node.name} (age {node.age}) [id: {node.id}]")

print("\n🔗 Edges:")
for edge in graph.list_edges():
    print(f"- {edge.type}: {edge.source} → {edge.target}")

from hgraph.core.hypergraph import Hypergraph
import graphviz
# -----------------------------
# Graphviz Visualizer
# -----------------------------


def to_graphviz(g: Hypergraph, filename="hypergraph", view=False):
    dot = graphviz.Digraph(comment="Hypergraph")

    # Add nodes
    for node in g.nodes.values():
        label = getattr(node, "name", getattr(node, "title", node.type))
        dot.node(str(node.id), label)

    # Add hyperedges
    for hyper in g.hyperedges.values():
        h_id = str(hyper.id)
        dot.node(h_id, "", shape="point")
        for src in hyper.sources:
            dot.edge(str(src), h_id)
        for tgt in hyper.targets:
            dot.edge(h_id, str(tgt))

    dot.render(filename, format="png", view=view)
    print(f"Graph rendered to {filename}.png")

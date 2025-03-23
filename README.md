# HGraph

```bash
hgraph/
│
├── core/
│   ├── __init__.py
│   ├── node.py          # contains Node base class
│   ├── edge.py          # contains Edge + Hyperedge classes
│   ├── config.py        # contains NodeConfig, EdgeConfig, HyperedgeConfig
│   ├── registry.py      # schema registry
│   ├── validator.py     # constraint checking logic
│   └── hypergraph.py    # Hypergraph implementation
```

# Project Status

## 1. Complete the Core API

**Next Steps:**
- [ ] `update_edge()` / `update_hyperedge()` should **re-validate** constraints.
- [ ] Support **directed multigraphs**: allow multiple edge types between same nodes.
- [ ] Allow **custom constraints**, e.g. via `@validator` on specific types.

---

## 2. Schema Registry + Persistence (Typed Saving & Loading)

**Current Status:**  
- We have dynamic runtime registration via `SchemaRegistry`.

**Next Steps:**
- [ ] Implement `save_to_json(path: str)` / `load_from_json(path: str)`
- [ ] Implement `save_to_parquet(path: str)` / `load_from_parquet(path: str)`
- [ ] Support **typed deserialization** using the registry
- [ ] Design a **SQLite backend adapter** with JSONB columns for flexibility
- [ ] Design a **DuckDB backend adapter**
- [ ] Add `export_schema()` to emit JSON Schema (for validation, tooling, docs)

---

## 3. Query Engine

Powerful querying is central to all knowledge systems.

**Design Options:**
- [ ] `find_edges(source=..., type=..., target=...)`
- [ ] `get_neighbors(node_id)`
- [ ] `find_path(start, end, max_depth=N)`
- [ ] `match(pattern: QueryPattern)` (think: basic Datalog-like DSL)

**Bonus:**
- [ ] Support filtering by config constraints (e.g. “only functional edges”)

---

## 4. Inference & Reasoning Layer

Once configs define all logical semantics, make them actionable.

**Capabilities to Add:**
- [ ] `infer_transitive_closure()` for transitive edges
- [ ] `auto_add_inverse_edges()` if `inverse` is set
- [ ] `check_consistency()` across the whole graph
- [ ] Constraint-based inferencing and validation at rest (like RDF validators)

---

## 5. Validation Suite & Developer Experience

**Goal:** Make it easy to test and extend.

- [ ] Add full `pytest` suite for:
  - Edges
  - Hyperedges
  - Constraint violations
  - Registry loading
- [ ] Enable `mypy` and `ruff` or `black` linting
- [ ] Provide CLI via `hgraph.cli` to:
  - Create/load graphs
  - Export to JSON/Graphviz
  - Validate graphs

---

## 6. Visualization & Introspection

- [ ] `.to_graphviz()` to generate .dot files
- [ ] Optional dependency for `networkx` export
- [ ] `.summary()` to list:
  - All registered types
  - Node/edge counts per type
  - Violations (if any)

---

## 7. Documentation

- [ ] Generate **Markdown docs** from model definitions (with constraints)
- [ ] Add tutorial notebooks or CLI walkthrough
- [ ] Auto-generate schemas for IDE support / OpenAPI-style UX

---

## Extensions & Frontier Features

### 1. Knowledge Graph Interoperability

- [ ] **Import RDF/OWL** and map classes/properties to `hgraph` `Node`/`Edge`/`Hyperedge` types
- [ ] **Export to RDF/OWL** from any `hgraph` graph
- [ ] Support **custom vocabularies** and **automatic type inference** when importing
- [ ] Ensure semantic compatibility with **SKOS**, **RDFS**, **OWL2**, and **Wikidata-style ontologies**

### 2. Graph Composition & Namespaces

- [ ] Define **namespaces** (like `core.person`, `finance.transaction`)
- [ ] Graphs can **declare dependencies** on other graphs (like modules or ontologies)
- [ ] Enable **merging** graphs under compatible or intersecting namespaces
- [ ] Namespace-specific **type resolution** and **IRI mapping** for RDF interop

### 3. Decentralized Graph Integration

- [ ] Allow teams to **fork** a graph and work on separate **branches**
- [ ] Introduce **merge requests** (MRs) between branches with:
  - Semantic diffing
  - Conflict detection
  - User-defined **merge strategies** (e.g., override, ignore, union)
- [ ] Design a **merge resolution layer** with interactive hooks

### 4. Schema Evolution & Migration

- [ ] Define **graph schema versions**
- [ ] Support **deprecations**, **renames**, **field migrations**, and **type changes**
- [ ] CLI tooling or migration DSL:
  ```bash
  hgraph migrate --from v1.0 --to v2.0
  ```

### 5. Temporal Graphs & Provenance

- [ ] Add **temporal dimensions** to edges/hyperedges (e.g., valid_from, valid_to)
- [ ] Integrate **provenance tracking**:
  - Who added this?
  - What source did it come from?
  - Which inference engine proposed it?

---

## Roadmap (Prioritized by Phase)

| Phase | Theme                                 | Deliverables |
|-------|----------------------------------------|--------------|
| ✅ 1  | **Constraint System**                 | Edge & Hyperedge validation |
| ✅ 2  | **Hypergraph Core API**               | CRUD, config-driven semantics |
| 🔜 3  | **Schema Registry + Typed Save/Load** | JSON + SQLite + schema-aware I/O |
| 🔜 4  | **Query Engine**                      | `.get_neighbors()`, `.find_by_type()`, etc. |
| 🔜 5  | **Graph Visualization**               | Graphviz, NetworkX, CLI-based |
| 🔜 6  | **Inference Layer**                   | Transitivity, Inverses, Closure |
| 🔜 7  | **Graph Composition**                 | Namespaces, Graph dependencies, Module loading |
| 🔜 8  | **RDF/OWL Interoperability**          | Import/export OWL/RDF → `hgraph` |
| 🔜 9  | **Branching, Merging, and Conflicts** | Merge Requests, Git-style ops |
| 🔜10  | **Schema Versioning + Migrations**    | DSL or config system for versioned graphs |
| 🔜11  | **Provenance + Temporal Reasoning**   | Time-bound relations, "who said what" support |

---

## Example: Graph Declaration

```python
class OpenAccountGraph(Hypergraph):
    namespace = "finance.accounting"
    dependencies = [
        GraphDependency(namespace="core.person", version=">=1.0.0"),
        GraphDependency(namespace="core.money", version="~2.1"),
    ]
```

---
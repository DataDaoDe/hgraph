from pydantic import BaseModel
from typing import Optional


class NodeConfig(BaseModel):
    pass


class EdgeConfig(BaseModel):
    """
    Configuration for binary edges.
    These flags define logical and structural properties of the relationship.

    Constraints like symmetric, reflexive, transitive, etc. describe possibility, not requirement.
    """

    symmetric: bool = False
    """
    If True:
        The edge relation is symmetric: if A → B exists, then B → A is logically valid.
        Example: "isSiblingOf" — if Alice is a sibling of Bob, then Bob is a sibling of Alice.
    If False:
        The reverse edge is not implied by the existence of the forward edge.
        Example: "isParentOf" — if Alice is a parent of Bob, Bob is not a parent of Alice.
    """

    antisymmetric: bool = False
    """
    If True:
        If A → B exists and B → A also exists, then A and B must be the same node (A == B).
        Example: "isAncestorOf" — if Alice is an ancestor of Bob and Bob is an ancestor of Alice, then Alice == Bob.
    If False:
        A → B and B → A can coexist even if A ≠ B.
        Example: "collaboratesWith" — mutual collaboration is allowed.
    """

    asymmetric: bool = False
    """
    If True:
        A → B means B → A is never allowed, even if A ≠ B.
        Example: "isBossOf" — if Alice is Bob’s boss, Bob cannot also be Alice’s boss.
    If False:
        Mutual links may exist.
        Example: "follows" on social media — mutual follows are possible.
    """

    reflexive: bool = False
    """
    If True:
        The edge may relate an entity to itself (A → A is allowed).
        Example: "trusts" — a person may trust themselves.
    If False:
        Self-edges are neither required nor explicitly forbidden.
        Use 'irreflexive' to prohibit them.
    """

    irreflexive: bool = False
    """
    If True:
        The edge must never relate an entity to itself (A → A is disallowed).
        Example: "isParentOf" — someone cannot be their own parent.
    If False:
        Self-links are permitted if allowed by other flags.
    """

    transitive: bool = False
    """
    If True:
        The relation supports transitive reasoning: A → B and B → C implies A → C.
        Example: "isAncestorOf" — ancestor chains can be inferred.
    If False:
        No transitive logic applies.
    """

    inverse: Optional[str] = None
    """
    The name of the inverse edge class, if any.
    Example: If this edge is 'HasChild', the inverse might be 'HasParent'.
    """

    functional: bool = False
    """
    If True:
        Each source node maps to at most one target for this edge type.
        Example: "hasBiologicalMother" — a person has exactly one biological mother.
    If False:
        The same source may link to multiple targets.
        Example: "hasFriend" — one person can have many friends.
    """

    inverse_functional: bool = False
    """
    If True:
        Each target node maps to at most one source.
        Example: "isSocialSecurityNumberOf" — each SSN is assigned to one person.
    If False:
        The same target may have multiple sources.
        Example: "livesIn" — many people can live in the same city.
    """


class HyperedgeConfig(BaseModel):
    """
    Configuration for n-ary (hyper)edges.

    These define semantics and structure for edges that connect more than two nodes.
    """

    unordered: bool = False
    """
    If True:
        The order of nodes in sources and targets does not matter.
        Example: "isInGroupWith" — Alice and Bob in a group is the same as Bob and Alice.
    If False:
        Order is meaningful and enforced.
        Example: "passedItemFromTo" — passing from A to B is not the same as B to A.
    """

    allows_duplicates: bool = False
    """
    If True:
        The same hyperedge can be inserted multiple times.
        Example: multiple people can join the same team multiple times (if modeled that way).
    If False:
        The same (sources, targets, type) cannot be added more than once.
        Example: "teachesCourse" — one professor cannot teach the same course twice in parallel.
    """

    cyclic: bool = False
    """
    If True:
        Nodes may appear in both sources and targets.
        Example: "isInRecursiveLoopWith" — valid for self-referencing logic.
    If False:
        A node may not be both a source and a target.
        Example: "transfersResourceTo" — one cannot transfer to oneself.
    """

    reflexive: bool = False
    """
    If True:
        The entire source set may equal the target set.
        Example: "coordinatesWith" — teams can coordinate internally with themselves.
    If False:
        The same set of nodes as source and target is disallowed.
    """

    functional: bool = False
    """
    If True:
        One unique source set may only map to one unique target set.
        Example: "hasOneOfficialDelegationFor" — one group can officially delegate to only one other group.
    If False:
        Sources may map to many different targets.
        Example: "collaboratedOnProjects" — one team can work on many projects.
    """

    inverse_functional: bool = False
    """
    If True:
        One unique target set may only be linked from one unique source set.
        Example: "authoredByTeam" — a paper can only be written by one team.
    If False:
        The same target set can be connected to multiple source sets.
        Example: "licensedTo" — a technology may be licensed to multiple entities.
    """

    transitive: bool = False
    """
    If True:
        The relation allows chaining logic across hyperedges.
        Example: "wasInfluencedBy" among philosophical schools.
    If False:
        No inferred connections may be made.
    """

    inverse: Optional[str] = None
    """
    Name of the inverse hyperedge type (if exists).
    Example: "DelegatesTo" <-> "ReceivesDelegationFrom"
    """

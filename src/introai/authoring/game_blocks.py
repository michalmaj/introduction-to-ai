"""Generated blocks for game trees: Mermaid drawings and alpha-beta trace tables.

    <!-- generated:game-tree example=worked_tree values=minimax -->
    <!-- generated:alpha-beta-table example=worked_tree lang=pl -->

``game-tree`` draws MAX nodes as ``▲`` and MIN nodes as ``▼``; leaves are
rounded and show their value for MAX. ``values=minimax`` adds the minimax value
of every inner node (with ``depth=N``: the tree cut off N moves deep, with the
estimates at the cutoff), ``values=alpha-beta`` what alpha-beta learned about
each node and which nodes it never visited. The thick edges are the moves both
players choose.
"""

from __future__ import annotations

import math
from collections import deque

from introai.games.examples import GAME_EXAMPLES, GAME_EXERCISES
from introai.games.reference import alpha_beta_search
from introai.games.trees import GameTree
from introai.trace import record


class GameBlockError(ValueError):
    """Raised for a game block that cannot be rendered; blocks.py reports it."""


_TEXT = {
    "pl": {
        "header": "| Krok | Węzeł | α | β | v | Co się stało |",
        "leaf": "liść",
        "return": "zwraca {v}",
        "cutoff_min": "odcięcie: v ≤ α, pominięte {skipped}",
        "cutoff_max": "odcięcie: v ≥ β, pominięte {skipped}",
        "summary": "Wartość korzenia: **{v}**, ruch: **{move}**. Pominięte liście: {pruned}.",
        "none": "brak",
    },
    "en": {
        "header": "| Step | Node | α | β | v | What happened |",
        "leaf": "leaf",
        "return": "returns {v}",
        "cutoff_min": "cutoff: v ≤ α, skipped {skipped}",
        "cutoff_max": "cutoff: v ≥ β, skipped {skipped}",
        "summary": "Root value: **{v}**, move: **{move}**. Pruned leaves: {pruned}.",
        "none": "none",
    },
}


def reveals_answers(kind: str, params: dict[str, str]) -> bool:
    """Whether a block would show the values or the pruning of a Part A tree."""
    if params.get("example") not in GAME_EXERCISES:
        return False
    return kind == "alpha-beta-table" or (kind == "game-tree" and "values" in params)


def _number(value: float) -> str:
    if value == math.inf:
        return "+∞"
    if value == -math.inf:
        return "−∞"
    return f"{value:g}".replace("-", "−")


def _tree(params: dict[str, str]) -> GameTree:
    name = params.get("example")
    if name not in GAME_EXAMPLES:
        raise GameBlockError(f"unknown example {name!r}")
    return GAME_EXAMPLES[name]()


def _mark(tree: GameTree, node: str) -> str:
    return "▲" if tree.to_move(node) == "MAX" else "▼"


def _levels(tree: GameTree, depth: int | None = None) -> list[str]:
    """Inner nodes to draw, level by level, down to ``depth`` moves below the root."""
    order, queue = [], deque([tree.initial])
    while queue:
        node = queue.popleft()
        if tree.is_terminal(node) or (depth is not None and tree.depth(node) >= depth):
            continue
        order.append(node)
        queue.extend(tree.actions(node))
    return order


def _principal_variation(tree: GameTree, best: dict[str, str]) -> set[tuple[str, str]]:
    edges, node = set(), tree.initial
    while node in best:
        edges.add((node, best[node]))
        node = best[node]
    return edges


def _minimax_labels(tree: GameTree, depth: int | None):
    """Labels of inner nodes and each node's best move, by minimax (cut off at ``depth``)."""
    labels: dict[str, str] = {}
    best: dict[str, str] = {}

    def value(node: str) -> float:
        if tree.is_terminal(node):
            return tree.leaves[node]
        if depth is not None and tree.depth(node) >= depth:
            if not tree.evaluations or node not in tree.evaluations:
                raise GameBlockError(f"no evaluation for {node!r} at depth {depth}")
            v = tree.evaluations[node]
            labels[node] = f"{_mark(tree, node)} {node}: e = {_number(v)}"
            return v
        values = {child: value(child) for child in tree.actions(node)}
        pick = max if tree.to_move(node) == "MAX" else min
        v = pick(values.values())
        best[node] = next(child for child, w in values.items() if w == v)
        labels[node] = f"{_mark(tree, node)} {node} = {_number(v)}"
        return v

    value(tree.initial)
    return labels, best


def _alpha_beta_labels(tree: GameTree):
    """Labels from what alpha-beta returned at each node, and the nodes it never visited."""
    with record(kinds={"alpha-beta"}) as trace:
        alpha_beta_search(tree, tree.initial)
    labels: dict[str, str] = {}
    for event in trace.of_kind("alpha-beta"):
        data = event.data
        node, v = data["node"], data["value"]
        if data["outcome"] == "leaf":
            continue
        low, high = data["window"]
        sign = "≤" if v <= low else "≥" if v >= high else "="
        labels[node] = f"{_mark(tree, node)} {node} {sign} {_number(v)}"
    visited = {event.data["node"] for event in trace.of_kind("alpha-beta")}
    return labels, _minimax_labels(tree, None)[1], visited


def _preorder(tree: GameTree) -> list[str]:
    order, stack = [], [tree.initial]
    while stack:
        node = stack.pop()
        order.append(node)
        stack.extend(reversed(tree.actions(node)))
    return order


def render_game_tree(params: dict[str, str]) -> str:
    tree = _tree(params)
    values = params.get("values")
    if values not in (None, "minimax", "alpha-beta"):
        raise GameBlockError(f"unknown values {values!r} (minimax or alpha-beta)")
    depth = None
    if "depth" in params:
        if values != "minimax":
            raise GameBlockError("depth=N works only with values=minimax")
        try:
            depth = int(params["depth"])
        except ValueError:
            raise GameBlockError(f"depth must be a whole number, got {params['depth']!r}") from None

    labels: dict[str, str] = {}
    best: dict[str, str] = {}
    visited: set[str] | None = None
    if values == "minimax":
        labels, best = _minimax_labels(tree, depth)
    elif values == "alpha-beta":
        labels, best, visited = _alpha_beta_labels(tree)

    thick = _principal_variation(tree, best)
    defined: set[str] = set()

    def node_text(node: str) -> str:
        if node in defined:
            return node
        defined.add(node)
        if tree.is_terminal(node):
            return f'{node}(["{node}: {_number(tree.leaves[node])}"])'
        return f'{node}["{labels.get(node, f"{_mark(tree, node)} {node}")}"]'

    lines = ["```mermaid", "graph TD"]
    for parent in _levels(tree, depth):
        for child in tree.actions(parent):
            arrow = "==>" if (parent, child) in thick else "-->"
            lines.append(f"    {node_text(parent)} {arrow} {node_text(child)}")
    if visited is not None:
        pruned = [node for node in _preorder(tree) if node not in visited]
        if pruned:
            lines += [
                "    classDef pruned stroke-dasharray: 5 4",
                f"    class {','.join(pruned)} pruned",
            ]
    lines.append("```")
    return "\n".join(lines)


def render_alpha_beta_table(params: dict[str, str]) -> str:
    lang = params.get("lang")
    if lang not in _TEXT:
        raise GameBlockError(f"unknown lang {lang!r}")
    tree = _tree(params)
    text = _TEXT[lang]
    with record(kinds={"alpha-beta", "utility"}) as trace:
        value, move = alpha_beta_search(tree, tree.initial)
    rows = []
    for step, event in enumerate(trace.of_kind("alpha-beta"), start=1):
        data = event.data
        node = data["node"]
        if data["outcome"] == "leaf":
            name, outcome = node, text["leaf"]
        else:
            name = f"{_mark(tree, node)} {node}"
            if data["outcome"] == "return":
                outcome = text["return"].format(v=_number(data["value"]))
            else:
                key = "cutoff_max" if tree.to_move(node) == "MAX" else "cutoff_min"
                outcome = text[key].format(skipped=", ".join(data["skipped"]))
        rows.append(
            f"| {step} | {name} | {_number(data['alpha'])} | {_number(data['beta'])} "
            f"| {_number(data['value'])} | {outcome} |"
        )
    seen = {event.data["state"] for event in trace.of_kind("utility")}
    pruned = [leaf for leaf in tree.leaves if leaf not in seen]
    separator = "|" + "---|" * (text["header"].count("|") - 1)
    summary = text["summary"].format(
        v=_number(value), move=move, pruned=", ".join(pruned) or text["none"]
    )
    return "\n".join([text["header"], separator, *rows]) + "\n\n" + summary

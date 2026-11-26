"""Drawing warehouse maps with matplotlib.

Colors follow a validated palette: expanded cells use categorical slot 1 (blue),
the path slot 2 (orange); obstacles are neutral ink and free floor is the
chart surface. The legend names the marks that are actually drawn.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING

import numpy as np

from introai.world.warehouse import Cell, WarehouseMap

if TYPE_CHECKING:
    from matplotlib.axes import Axes

SURFACE = "#fcfcfb"
OBSTACLE = "#52514e"
EXPANDED = "#2a78d6"
PATH = "#eb6834"
INK = "#0b0b0b"

_FLOOR, _OBSTACLE, _EXPANDED, _PATH = range(4)


def plot_map(
    warehouse: WarehouseMap,
    *,
    path: Sequence[Cell] = (),
    expanded: Iterable[Cell] = (),
    title: str | None = None,
    ax: Axes | None = None,
    expanded_label: str = "expanded",
) -> Axes:
    """Draw the map, the expanded cells and the path; return the axes."""
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import Patch

    if ax is None:
        _, ax = plt.subplots(figsize=(warehouse.cols * 0.35 + 1.8, warehouse.rows * 0.35 + 0.6))

    grid = np.full((warehouse.rows, warehouse.cols), _FLOOR)
    expanded_cells = list(expanded)
    for cell in expanded_cells:
        grid[cell] = _EXPANDED
    for cell in path:
        grid[cell] = _PATH
    for cell in warehouse.walls:
        grid[cell] = _OBSTACLE

    cmap = ListedColormap([SURFACE, OBSTACLE, EXPANDED, PATH])
    ax.imshow(grid, cmap=cmap, vmin=0, vmax=3, interpolation="nearest")

    # A thin surface-colored gap between cells keeps neighbouring fills apart.
    ax.set_xticks(np.arange(-0.5, warehouse.cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, warehouse.rows, 1), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=1.5)
    ax.tick_params(which="both", length=0, labelbottom=False, labelleft=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    labels = [("R", warehouse.start), ("D", warehouse.dock)]
    labels += [("P", cell) for cell in sorted(warehouse.parcels)]
    for label, (row, col) in labels:
        ax.text(
            col,
            row,
            label,
            ha="center",
            va="center",
            fontsize=8,
            fontweight="bold",
            color=INK,
            bbox={"boxstyle": "round,pad=0.15", "facecolor": SURFACE, "edgecolor": "none"},
        )

    handles = [Patch(facecolor=OBSTACLE, label="obstacle")]
    if expanded_cells:
        handles.append(Patch(facecolor=EXPANDED, label=expanded_label))
    if path:
        handles.append(Patch(facecolor=PATH, label="path"))
    ax.legend(
        handles=handles,
        loc="upper left",
        bbox_to_anchor=(1.01, 1.0),
        frameon=False,
        fontsize=8,
        labelcolor=INK,
    )
    if title is not None:
        ax.set_title(title, fontsize=10, color=INK)
    return ax

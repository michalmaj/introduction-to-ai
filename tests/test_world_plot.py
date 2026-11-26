from introai.world.plot import plot_map
from introai.world.warehouse import WarehouseMap

SMALL = "#######\n#R..#.#\n#.#...#\n#...#D#\n#######"


def test_plot_map_draws_grid():
    ax = plot_map(WarehouseMap.from_text(SMALL), path=[(1, 1)], title="small")
    assert ax.images[0].get_array().shape == (5, 7)
    assert ax.get_title() == "small"


def test_plot_map_has_legend_and_start_dock_labels():
    m = WarehouseMap.from_text(SMALL)
    ax = plot_map(m, path=[(1, 1), (1, 2)], expanded=[(2, 1)])
    legend_labels = [t.get_text() for t in ax.get_legend().get_texts()]
    assert legend_labels == ["obstacle", "expanded", "path"]
    assert {t.get_text() for t in ax.texts} == {"R", "D"}


def test_plot_map_labels_parcels():
    m = WarehouseMap.from_text("#######\n#R.P#P#\n#.#...#\n#..P#D#\n#######")
    ax = plot_map(m)
    assert sorted(t.get_text() for t in ax.texts) == ["D", "P", "P", "P", "R"]


def test_plot_map_legend_lists_only_what_is_drawn():
    m = WarehouseMap.from_text(SMALL)
    labels = lambda ax: [t.get_text() for t in ax.get_legend().get_texts()]  # noqa: E731
    assert labels(plot_map(m)) == ["obstacle"]
    assert labels(plot_map(m, expanded=[(2, 1)])) == ["obstacle", "expanded"]
    assert labels(plot_map(m, path=[(1, 1)])) == ["obstacle", "path"]


def test_plot_map_can_rename_the_expanded_mark():
    m = WarehouseMap.from_text(SMALL)
    ax = plot_map(m, expanded=[(2, 1)], expanded_label="visited")
    assert [t.get_text() for t in ax.get_legend().get_texts()] == ["obstacle", "visited"]

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

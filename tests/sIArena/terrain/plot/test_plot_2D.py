import unittest
from unittest.mock import patch

from sIArena.terrain.Terrain import Terrain
from sIArena.terrain.plot.plot_2D import plot_terrain_2D


class TestPlotTerrain2D(unittest.TestCase):
    def test_plots_terrain_markers_paths_and_legend(self):
        terrain = Terrain([[1, 2], [3, 4]])
        path = [(0, 0), (0, 1), (1, 1)]

        with patch("sIArena.terrain.plot.plot_2D.plt") as plt_mock:
            plot_terrain_2D(
                terrain,
                path=path,
                paths_legends=["best"],
                add_cost_to_legend=True,
                title="Example",
            )

        plt_mock.clf.assert_called_once()
        plt_mock.imshow.assert_called_once_with(terrain.matrix, cmap="terrain")
        self.assertEqual(plt_mock.plot.call_args_list[0].args, (0, 0, "r+"))
        self.assertEqual(plt_mock.plot.call_args_list[1].args, (1, 1, "rx"))
        self.assertEqual(plt_mock.plot.call_args_list[2].args[:3], ([0, 1, 1], [0, 0, 1], "r"))
        self.assertEqual(plt_mock.plot.call_args_list[2].kwargs["label"], "best (6)")
        plt_mock.legend.assert_called_once()
        plt_mock.title.assert_called_once_with("Example")
        plt_mock.show.assert_called_once_with(block=False)
        plt_mock.pause.assert_called_once_with(0.001)

    def test_skips_legend_when_not_requested(self):
        terrain = Terrain([[1, 2], [3, 4]])

        with patch("sIArena.terrain.plot.plot_2D.plt") as plt_mock:
            plot_terrain_2D(terrain, paths=[[(0, 0), (1, 0), (1, 1)]])

        plt_mock.legend.assert_not_called()

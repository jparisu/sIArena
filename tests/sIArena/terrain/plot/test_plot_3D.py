import unittest
from unittest.mock import patch

from sIArena.terrain.Terrain import Terrain
from sIArena.terrain.plot.plot_3D import plot_terrain_3D


class FakeAxes:
    def __init__(self):
        self.view_init_calls = []
        self.plot_surface_calls = []
        self.plot_calls = []
        self.xlim = None
        self.ylim = None
        self.zlim = None
        self.xlabel = None
        self.ylabel = None
        self.title = None

    def view_init(self, *args):
        self.view_init_calls.append(args)

    def set_title(self, title):
        self.title = title

    def plot_surface(self, *args, **kwargs):
        self.plot_surface_calls.append((args, kwargs))

    def plot(self, *args, **kwargs):
        self.plot_calls.append((args, kwargs))

    def set_xlim(self, *args):
        self.xlim = args

    def set_ylim(self, *args):
        self.ylim = args

    def set_zlim(self, *args):
        self.zlim = args

    def set_xlabel(self, label):
        self.xlabel = label

    def set_ylabel(self, label):
        self.ylabel = label


class FakeFigure:
    def __init__(self):
        self.axes = []
        self.title = None

    def add_subplot(self, *args, **kwargs):
        axis = FakeAxes()
        self.axes.append((args, kwargs, axis))
        return axis

    def suptitle(self, title):
        self.title = title


class TestPlotTerrain3D(unittest.TestCase):
    def test_plots_surface_origin_destination_and_paths_for_each_angle(self):
        terrain = Terrain([[1, 2], [3, 4]])
        figure = FakeFigure()

        with patch("sIArena.terrain.plot.plot_3D.plt.figure", return_value=figure) as figure_mock:
            with patch("sIArena.terrain.plot.plot_3D.plt.show") as show_mock:
                plot_terrain_3D(terrain, path=[(0, 0), (1, 0), (1, 1)], title="3D")

        figure_mock.assert_called_once_with(figsize=(18, 6))
        self.assertEqual(len(figure.axes), 2)
        first_axis = figure.axes[0][2]
        self.assertEqual(first_axis.view_init_calls[0], (45, 45))
        self.assertEqual(first_axis.title, "Angle (45, 45)")
        self.assertEqual(len(first_axis.plot_surface_calls), 1)
        self.assertEqual(first_axis.plot_calls[0][0][:3], ([0], [0], [1]))
        self.assertEqual(first_axis.plot_calls[1][0][:3], ([1], [1], [4]))
        self.assertEqual(first_axis.plot_calls[2][0][:3], ([0, 1, 1], [0, 0, 1], [1, 3, 4]))
        self.assertEqual(first_axis.xlabel, "row")
        self.assertEqual(first_axis.ylabel, "col")
        self.assertEqual(figure.title, "3D")
        show_mock.assert_called_once_with()

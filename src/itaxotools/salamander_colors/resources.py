from PySide6 import QtCore, QtGui

from enum import Enum
from pathlib import Path

from itaxotools.common.widgets import VectorPixmap
from itaxotools.taxi_gui.app import skin
from itaxotools.taxi_gui.app.resources import LazyResourceCollection


class Size(Enum):
    Large = QtCore.QSize(128, 128)
    Medium = QtCore.QSize(64, 64)
    Small = QtCore.QSize(16, 16)

    def __init__(self, size):
        self.size = size


def get_data(path: str):
    here = Path(__file__).parent
    return str(here / path)


icons = LazyResourceCollection(
    salamander_colors=lambda: QtGui.QIcon(get_data("graphics/salamander.ico")),
)

pixmaps = LazyResourceCollection(
    salamander_colors=lambda: VectorPixmap(
        get_data("graphics/salamander.svg"),
        colormap=skin.colormap_icon,
    ),
)

pixmaps_graphics = LazyResourceCollection(
    arrow=lambda: VectorPixmap(get_data("graphics/arrow.svg"), size=QtCore.QSize(8, 16)),
    arrow_mirrored=lambda: VectorPixmap(get_data("graphics/arrow.svg"), size=QtCore.QSize(8, 16)).transformed(
        QtGui.QTransform().scale(-1, 1)
    ),
    dot=lambda: VectorPixmap(get_data("graphics/dot.svg"), size=QtCore.QSize(8, 16)),
)

task_pixmaps_large = LazyResourceCollection(
    measure=lambda: VectorPixmap(get_data("graphics/salamander.svg"), Size.Large.size, colormap=skin.colormap_icon),
)

task_pixmaps_medium = LazyResourceCollection(
    measure=lambda: VectorPixmap(get_data("graphics/salamander.svg"), Size.Medium.size, colormap=skin.colormap_icon),
)

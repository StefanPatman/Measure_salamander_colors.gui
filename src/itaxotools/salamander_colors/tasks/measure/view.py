from PySide6 import QtWidgets

from pathlib import Path

from itaxotools.common.utility import AttrDict
from itaxotools.taxi_gui import app
from itaxotools.taxi_gui.tasks.common.view import ProgressCard
from itaxotools.taxi_gui.view.cards import Card

from ..common.view import (
    GraphicTitleCard,
    PathDirectorySelector,
    PathFileOutSelector,
    SalamanderTaskView,
)
from ..common.widgets import IntPropertyLineEdit, PropertyLineEdit
from . import long_description, pixmap_medium, title


class OptionsCard(Card):
    def __init__(self, parent=None):
        super().__init__(parent)

        label = QtWidgets.QLabel("Options:")
        label.setStyleSheet("font-size: 16px;")
        label.setMinimumWidth(150)

        description = QtWidgets.QLabel("Pixel classification thresholds and image file extension.")

        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(label)
        title_layout.addWidget(description, 1)
        title_layout.setSpacing(16)

        grid = QtWidgets.QGridLayout()
        grid.setColumnMinimumWidth(0, 16)
        grid.setColumnMinimumWidth(1, 160)
        grid.setColumnStretch(3, 1)
        grid.setHorizontalSpacing(32)
        grid.setVerticalSpacing(8)

        row = 0

        grid.addWidget(QtWidgets.QLabel("Extension:"), row, 1)
        extension_field = PropertyLineEdit()
        extension_field.setFixedWidth(100)
        extension_field.setPlaceholderText(".JPG")
        grid.addWidget(extension_field, row, 2)
        grid.addWidget(QtWidgets.QLabel("File extension of image files (e.g. .JPG, .png)"), row, 3)
        self.controls.extension = extension_field
        row += 1

        grid.addWidget(QtWidgets.QLabel("Background:"), row, 1)
        background_field = IntPropertyLineEdit()
        background_field.setFixedWidth(100)
        grid.addWidget(background_field, row, 2)
        grid.addWidget(QtWidgets.QLabel("Minimum R, G, B value for a pixel to be classified as background"), row, 3)
        self.controls.background_threshold = background_field
        row += 1

        grid.addWidget(QtWidgets.QLabel("Black:"), row, 1)
        black_field = IntPropertyLineEdit()
        black_field.setFixedWidth(100)
        grid.addWidget(black_field, row, 2)
        grid.addWidget(QtWidgets.QLabel("Maximum R, G, B value for a pixel to be classified as black"), row, 3)
        self.controls.black_threshold = black_field
        row += 1

        self.addLayout(title_layout)
        self.addLayout(grid)


class View(SalamanderTaskView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw_cards()

    def draw_cards(self):
        self.cards = AttrDict()
        self.cards.title = GraphicTitleCard(title, long_description, pixmap_medium.resource, self)
        self.cards.progress = ProgressCard(self)
        self.cards.input = PathDirectorySelector("Input folder", "in", self)
        self.cards.output = PathFileOutSelector("Output file", "out", self)
        self.cards.options = OptionsCard(self)

        self.cards.input.set_placeholder_text("Folder containing salamander image files")
        self.cards.output.set_placeholder_text("Results will be saved here (tab-delimited)")

        layout = QtWidgets.QVBoxLayout()
        for card in self.cards:
            layout.addWidget(card)
        layout.addStretch(1)
        layout.setSpacing(6)
        layout.setContentsMargins(6, 6, 6, 6)

        self.setLayout(layout)

    def setObject(self, object):
        self.object = object
        self.binder.unbind_all()

        self.binder.bind(object.notification, self.showNotification)
        self.binder.bind(object.report_results, self.report_results)
        self.binder.bind(object.progression, self.cards.progress.showProgress)
        self.binder.bind(object.properties.busy, self.cards.progress.setVisible)

        self.binder.bind(object.properties.input_path, self.cards.input.set_path)
        self.binder.bind(self.cards.input.selectedPath, object.properties.input_path)

        self.binder.bind(object.properties.output_path, self.cards.output.set_path)
        self.binder.bind(self.cards.output.selectedPath, object.properties.output_path)

        self.cards.options.controls.extension.bind_property(object.properties.extension)
        self.cards.options.controls.background_threshold.bind_property(object.properties.background_threshold)
        self.cards.options.controls.black_threshold.bind_property(object.properties.black_threshold)

        self.binder.bind(object.properties.editable, self.setEditable)

    def setEditable(self, editable: bool):
        for card in self.cards:
            card.setEnabled(editable)
        self.cards.title.setEnabled(True)
        self.cards.progress.setEnabled(True)

    def open(self):
        filename = QtWidgets.QFileDialog.getExistingDirectory(
            parent=self.window(),
            caption=f"{app.config.title} - Open folder",
        )
        if not filename:
            return
        self.object.open(Path(filename))

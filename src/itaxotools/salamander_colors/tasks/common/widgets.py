from PySide6 import QtCore, QtGui, QtWidgets

from typing import Literal

from itaxotools.common.bindings import Binder, PropertyRef
from itaxotools.taxi_gui.utility import type_convert

from itaxotools.salamander_colors.resources import pixmaps_graphics


class ElidedLineEdit(QtWidgets.QLineEdit):
    textDeleted = QtCore.Signal()

    def keyPressEvent(self, event):
        if event.key() in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
            if self.text():
                self.textDeleted.emit()
                return
        super().keyPressEvent(event)


class IOLabel(QtWidgets.QWidget):
    def __init__(self, text="", direction: Literal["in", "out", "?"] = "in", parent=None):
        super().__init__(parent)

        pixmap = {
            "in": pixmaps_graphics.arrow,
            "out": pixmaps_graphics.arrow_mirrored,
            "?": pixmaps_graphics.dot,
        }.get(direction, pixmaps_graphics.dot)

        self.arrow = QtWidgets.QLabel()
        self.arrow.setPixmap(pixmap.resource)
        self.arrow.setFixedWidth(8)

        self.label = QtWidgets.QLabel(f"{text}:")
        self.label.setStyleSheet("font-size: 16px;")

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(self.arrow)
        layout.addWidget(self.label)

        self.setMinimumWidth(150)

    def setText(self, text):
        self.label.setText(f"{text}:")

    def text(self):
        text = self.label.text()
        return text[:-1] if text.endswith(":") else text


class BasePropertyLineEdit(QtWidgets.QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.binder = Binder()
        self.proxy_in = lambda x: str(x) if x is not None else ""
        self.proxy_out = lambda x: x

    def bind_property(self, property: PropertyRef):
        self.binder.unbind_all()
        self.binder.bind(property, self.setText, proxy=self.proxy_in)
        self.binder.bind(self.textEdited, property, proxy=self.proxy_out)


class PropertyLineEdit(BasePropertyLineEdit):
    def bind_property(self, property: PropertyRef):
        super().bind_property(property)
        self.setPlaceholderText(self.proxy_in(property.default))


class IntPropertyLineEdit(PropertyLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy_in = lambda x: type_convert(x, str, "")
        self.proxy_out = lambda x: type_convert(x, int, 0)
        self.setValidator(QtGui.QIntValidator())

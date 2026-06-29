from itaxotools.common.utility import override
from itaxotools.taxi_gui.main import Main as _Main


class Main(_Main):
    @override
    def draw(self):
        super().draw()
        self.widgets.header.toolLogo.hide()

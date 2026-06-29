from PySide6 import QtCore

from itaxotools.taxi_gui.model.tasks import TaskModel
from itaxotools.taxi_gui.threading import ReportDone, ReportStop

from .types import Results


class SalamanderTaskModel(TaskModel):
    report_results = QtCore.Signal(str, Results)

    def onDone(self, report: ReportDone):
        self.report_results.emit(self.task_name.replace("_", " "), report.result)
        self.busy = False

    def onStop(self, report: ReportStop):
        self.busy = False

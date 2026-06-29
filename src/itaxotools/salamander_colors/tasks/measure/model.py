from pathlib import Path

from itaxotools.common.bindings import Property
from itaxotools.taxi_gui.model.tasks import SubtaskModel

from ..common.model import SalamanderTaskModel
from . import process, title


class Model(SalamanderTaskModel):
    task_name = title

    input_path = Property(Path, Path())
    output_path = Property(Path, Path())
    extension = Property(str, ".JPG")
    background_threshold = Property(int, 120)
    black_threshold = Property(int, 120)

    def __init__(self, name=None):
        super().__init__(name)
        self.can_open = True
        self.can_save = False

        self.binder.bind(
            self.properties.input_path,
            self.properties.output_path,
            lambda p: p / "Salamander_color_results.tsv" if p != Path() else Path(),
        )

        self.subtask_init = SubtaskModel(self, bind_busy=False)

        for handle in [
            self.properties.input_path,
            self.properties.output_path,
            self.properties.extension,
        ]:
            self.binder.bind(handle, self.checkReady)
        self.checkReady()

        self.subtask_init.start(process.initialize)

    def isReady(self):
        if self.input_path == Path():
            return False
        if self.output_path == Path():
            return False
        if not self.extension:
            return False
        return True

    def start(self):
        super().start()
        self.exec(
            process.execute,
            input_path=self.input_path,
            output_path=self.output_path,
            extension=self.extension,
            background_threshold=self.background_threshold,
            black_threshold=self.black_threshold,
        )

    def open(self, path: Path):
        if path.is_dir():
            self.input_path = path
        else:
            self.input_path = path.parent

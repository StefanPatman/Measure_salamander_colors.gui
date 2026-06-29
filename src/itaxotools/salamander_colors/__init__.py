"""GUI entry point"""

import multiprocessing


def run():
    from itaxotools.taxi_gui.app import Application, skin

    from . import config
    from .main import Main

    app = Application()
    app.set_config(config)
    app.set_skin(skin)

    main = Main()
    main.resize(720, 520)
    main.setMinimumWidth(640)
    main.show()

    app.exec()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run()

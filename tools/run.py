"""PyInstaller entry point"""

import multiprocessing

from itaxotools.salamander_colors import run

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run()

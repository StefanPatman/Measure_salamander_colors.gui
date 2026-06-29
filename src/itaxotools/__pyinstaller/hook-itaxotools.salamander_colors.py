from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = collect_data_files("itaxotools.salamander_colors")

hiddenimports = collect_submodules("itaxotools.salamander_colors.tasks", filter=lambda name: True)

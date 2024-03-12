from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from PySide6 import QtCore, QtWidgets, QtGui
from rich.console import Console

from cyberdrop_dl import __version__

console = Console()

if TYPE_CHECKING:
    from cyberdrop_dl.managers.manager import Manager

def program_gui(manager: Manager):
    """Program GUI"""
    app = QtWidgets.QApplication([])

    widget = window_main(manager)
    widget.setWindowTitle("CyberDrop Downloader")
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

class tab_config(QtWidgets.QtWidget):
    def __init__(self, file_info: QFileInfo, parent: QWidget):
        super().__init__(parent)
        #loop through all elements in file_info, create textboxes and whatnot
        self.tab_box = QtWidgets.QVBoxLayout()
        #section title
        self.tab_box.addWidget(QtWidgets.QLabel(""))
        while False:
            self.widget_row = QtWidgets.QHBoxLayout()
            self.widget_row.addWidget(QtWidgets.QLabel("key"))
            #text
            self.widget_row.addWidget(QtWidgets.QLineEdit())
            #int

            #float

            #bool

            #filepicker

            #folderpicker



class window_main(QtWidgets.QtWidget):
    def __init__(self, manger: Manager):
        super().__init__()

        console.clear()
        console.print(f"[bold]Cyberdrop Downloader (V{str(__version__)})[/bold]")
        console.print(f"[bold]Current Config:[/bold] {manager.config_manager.loaded_config}")

        self.button_global_save = QtWidgets.QPushButton("Save")
        self.button_global_reset = QtWidgets.QPushButton("Reset")

        self.button_authentication_save = QtWidgets.QPushButton("Save")
        self.button_authentication_reset = QtWidgets.QPushButton("Reset")

        self.tab_bar_config = QTabWidget()
        # self.tab_bar_config.addTab(tab_config(file_info, self), file_info.fileName())
        self.button_config_save = QtWidgets.QPushButton("Save")
        self.button_config_reset = QtWidgets.QPushButton("Reset")
        self.button_config_run = QtWidgets.QPushButton("Run")
        self.button_config_run_all = QtWidgets.QPushButton("Run all")

        self.button_update = QtWidgets.QPushButton("Update")

        self.layout = QtWidgets.QVBoxLayout(self)

    # Download
    @QtCore.Slot()
    def action_download(self):
        pass
    
    # Download (All Configs)
    @QtCore.Slot()
    def action_download_all(self):
        manager.args_manager.all_configs = True
        pass

    # Retry Failed Downloads
    @QtCore.Slot()
    def action_retry(self):
        manager.args_manager.retry = True
        pass

    # Edit URLs
    @QtCore.Slot()
    def action_edit_URLs(self):
        input_file = manager.config_manager.settings_data['Files']['input_file'] if not manager.args_manager.input_file else manager.args_manager.input_file
        edit_urls_prompt(input_file, manager.vi_mode)
        pass

    # Select Config
    @QtCore.Slot()
    def action_select_config(self):
        configs = manager.config_manager.get_configs()
        selected_config = select_config_prompt(manager, configs)
        manager.config_manager.change_config(selected_config)

    @QtCore.Slot()
    def action_edit_input_output(self):
        console.clear()
        console.print("Editing Input / Output File Paths")
        input_file = inquirer.filepath(
            message="Enter the input file path:",
            default=str(manager.config_manager.settings_data['Files']['input_file']),
            validate=PathValidator(is_file=True, message="Input is not a file"),
            vi_mode=manager.vi_mode,
        ).execute()
        download_folder = inquirer.text(
            message="Enter the download folder path:",
            default=str(manager.config_manager.settings_data['Files']['download_folder']),
            validate=PathValidator(is_dir=True, message="Input is not a directory"),
            vi_mode=manager.vi_mode,
        ).execute()

        manager.config_manager.settings_data['Files']['input_file'] = Path(input_file)
        manager.config_manager.settings_data['Files']['download_folder'] = Path(download_folder)
        manager.config_manager.write_updated_settings_config()
        pass

    # Manage Configs
    @QtCore.Slot()
    def action_manage_configs(self):
        while True:
            console.clear()
            console.print("[bold]Manage Configs[/bold]")
            console.print(f"[bold]Current Config:[/bold] {manager.config_manager.loaded_config}")

            action = manage_configs_prompt(manager)

            # Change Default Config
            if action == 1:
                configs = manager.config_manager.get_configs()
                selected_config = select_config_prompt(configs)
                manager.config_manager.change_default_config(selected_config)

            # Create A Config
            elif action == 2:
                create_new_config_prompt(manager)

            # Delete A Config
            elif action == 3:
                configs = manager.config_manager.get_configs()
                if len(configs) != 1:
                    selected_config = select_config_prompt(configs)
                    if selected_config == manager.config_manager.loaded_config:
                        inquirer.confirm(
                            message="You cannot delete the currently active config, press enter to continue.",
                            default=False,
                            vi_mode=manager.vi_mode,
                        ).execute()
                        continue
                    manager.config_manager.delete_config(selected_config)
                else:
                    inquirer.confirm(
                        message="There is only one config, press enter to continue.",
                        default=False,
                        vi_mode=manager.vi_mode,
                    ).execute()

            # Edit Config
            elif action == 4:
                edit_config_values_prompt(manager)

            # Edit Authentication Values
            elif action == 5:
                edit_authentication_values_prompt(manager)

            # Edit Global Settings
            elif action == 6:
                edit_global_settings_prompt(manager)

            # Done
            elif action == 7:
                break
        pass

    # Import Cyberdrop_V4 Items
    @QtCore.Slot()
    def action_import_v4(self):
        import_cyberdrop_v4_items_prompt(manager)
        pass

    # Donate
    @QtCore.Slot()
    def action_donate(self):
        donations_prompt(manager)
        pass

    # Exit
    @QtCore.Slot()
    def action_exit(self):
        exit(0)

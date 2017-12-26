import os
from interfaces.cli import menu
from settings import settings
from interfaces.gui.guimanager import GuiProcessManager, ELECTRON_PATH

def create_ui_manager():
    use_gui = settings['interface'] == 'gui'
    if use_gui and not os.path.isfile(ELECTRON_PATH):
        print(f"Can't find electron path: {ELECTRON_PATH}")
        use_gui = False
    ui_manager = GuiProcessManager() if use_gui else menu.MainMenu().start
    return ui_manager

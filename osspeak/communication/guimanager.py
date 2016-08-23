import subprocess

class GuiManager:
    
    def __init__(self):
        pass
        # self.electron_process = subprocess.Popen

    def launch(self):
        self.electron_process = subprocess.Popen(['npm', 'start'], cwd=r'C:\Users\evan\modules\osspeak\gui', shell=True)

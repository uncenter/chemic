import os
import subprocess
from pathlib import Path
import nicegui

static_dir = Path(nicegui.__file__).parent
parameters = '--onefile main.py --name "chemic" ' + \
    f'--add-data="{static_dir}{os.pathsep}nicegui" --collect-all chemic'

subprocess.call('pyinstaller ' + parameters, shell=True)
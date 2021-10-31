import sys
from pathlib import Path


def get_path(path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    path = Path(path)
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
        path = path.name
    except AttributeError:
        base_path = Path(__file__).parent.resolve()

    return str(base_path / path)

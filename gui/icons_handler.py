import sys
from pathlib import Path
import actions

ACTION_ICONS = {actions.ClickAction: 'icons/input-mouse.svg',
                actions.MoveCursorAction: 'icons/transform-move.svg',
                actions.CursorPathAction: 'icons/path-mode-polyline.svg',
                actions.PressKeyAction: 'icons/input-keyboard.svg',
                actions.WriteTextAction: 'icons/edit-select-text.svg',
                actions.PauseAction: 'icons/media-playback-pause.svg',
                actions.LoopAction: 'icons/gtk-convert.svg'}


def get_icon_path(path: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    path = Path(path)
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
        path = path.name
    except AttributeError:
        base_path = Path(__file__).parent.resolve()

    return str(base_path / path)


def get_action_icon(action_class) -> str:
    return ACTION_ICONS.get(action_class, 'icons/data-error.svg')

from collections import defaultdict

import actions

ACTION_ICONS = defaultdict(lambda: 'icons/data-error.svg', {actions.ClickAction: 'gui/icons/input-mouse.svg',
                                                            actions.MoveCursorAction: 'gui/icons/transform-move.svg',
                                                            actions.CursorPathAction: 'gui/icons/path-mode-polyline.svg',
                                                            actions.PressKeyAction: 'gui/icons/input-keyboard.svg',
                                                            actions.WriteTextAction: 'gui/icons/edit-select-text.svg',
                                                            actions.PauseAction: 'gui/icons/media-playback-pause.svg',
                                                            actions.LoopAction: 'gui/icons/gtk-convert.svg',
                                                            actions.GotoAction: 'gui/icons/gtk-convert.svg'})


def get_action_icon(action_cls) -> str:
    return ACTION_ICONS[action_cls]

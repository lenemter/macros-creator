def convert_name(name: str):
    # e.g write_text -> Write text
    return name.capitalize().replace('_', ' ')


def convert_settings(settings: dict):
    """Convert settings to needed type"""
    # noinspection PyTypeChecker
    settings['time_between'] = float(settings.get('time_between', 0.0))

    return settings


def read_file_xml(filepath) -> tuple:
    import xml.etree.ElementTree as ElementTree
    from .utils import NAME_CLASS_DICT

    actions = []
    tree = ElementTree.parse(filepath)
    root = tree.getroot()
    settings = root.attrib
    for child in list(root):
        child = child
        tag = child.tag
        attrib = child.attrib
        action_cls = NAME_CLASS_DICT[convert_name(tag)]
        action = action_cls(**attrib)  # create action
        actions.append(action)

    settings = convert_settings(settings)

    return actions, settings

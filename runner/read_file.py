from .utils import NAME_CLASS_DICT


def read_file_xml(filepath) -> tuple:
    import xml.etree.ElementTree as ElementTree

    actions = []
    tree = ElementTree.parse(filepath)
    root = tree.getroot()
    settings = root.attrib
    for child in list(root):
        child = child
        tag = child.tag
        attrib = child.attrib
        action_cls = NAME_CLASS_DICT[tag.capitalize().replace('_', ' ')]
        action = action_cls(**attrib)  # create action
        actions.append(action)

    # noinspection PyTypeChecker
    settings['time_between'] = float(settings['time_between'])

    return actions, settings


def read_file_csv(filepath) -> tuple:
    import csv

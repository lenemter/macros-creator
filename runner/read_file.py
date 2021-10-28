from .utils import NAME_CLASS_DICT


def read_file_xml(filepath) -> tuple:
    import xml.etree.ElementTree as ET

    actions_list = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    settings = root.attrib
    for child in list(root):
        child = child
        tag = child.tag
        attrib = child.attrib
        action = NAME_CLASS_DICT[tag.capitalize().replace('_', ' ')](**attrib)  # create action
        actions_list.append(action)

    # noinspection PyTypeChecker
    settings['time_between'] = float(settings['time_between'])

    return actions_list, settings


def read_file_db(filepath) -> tuple:
    import sqlite3

    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    settings = cursor.execute('SELECT name, value FROM settings').fetchall()
    actions_list = cursor.execute('SELECT name, parameters FROM macro').fetchall()
    connection.close()

    settings = {key: value for (key, value) in settings}
    # noinspection PyTypeChecker
    settings['time_between'] = float(settings['time_between'])

    actions_list = []

    print(f'{settings=} {actions_list=}')

    return actions_list, settings

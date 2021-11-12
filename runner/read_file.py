def convert_name(name: str):
    return name.capitalize().replace('_', ' ')


def convert_settings(settings: dict):
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


def read_file_csv(filepath) -> tuple:
    import csv
    from .utils import NAME_CLASS_DICT, DELIMITER, QUOTECHAR, QUOTE_METHOD

    actions = []
    with open(filepath, mode='r', encoding='UTF-8') as file:
        reader = csv.reader(file, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTE_METHOD)
        for row in reader:
            settings = row[1:]
            break
        settings = [parameter.split('=') for parameter in settings]
        settings = {parameter: value for (parameter, value) in settings}
        settings = convert_settings(settings)

        for row in reader:
            name, *parameters = row
            name = convert_name(name)
            parameters = [parameter.split('=') for parameter in parameters]
            parameters = {parameter: value for (parameter, value) in parameters}

            action_cls = NAME_CLASS_DICT[name]
            actions.append(action_cls(**parameters))

    return actions, settings


def read_file_db(filepath) -> tuple:
    from io import StringIO
    import csv
    import sqlite3
    from .utils import NAME_CLASS_DICT, DELIMITER, QUOTECHAR, QUOTE_METHOD

    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    settings = cursor.execute('SELECT settings FROM settings').fetchall()
    actions = cursor.execute('SELECT action FROM macro').fetchall()
    connection.close()

    settings = settings[0][0]
    actions = '\n'.join([x[0] for x in actions])
    data = StringIO(settings + '\n' + actions)
    print(f'{data.getvalue()=}')
    reader = csv.reader(data, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTE_METHOD)
    actions = []
    for row in reader:
        settings = row[1:]
        break
    settings = [parameter.split('=') for parameter in settings]
    settings = {parameter: value for (parameter, value) in settings}
    settings = convert_settings(settings)

    for row in reader:
        name, *parameters = row
        name = convert_name(name)
        parameters = [parameter.split('=') for parameter in parameters]
        parameters = {parameter: value for (parameter, value) in parameters}

        action_cls = NAME_CLASS_DICT[name]
        actions.append(action_cls(**parameters))

    return actions, settings

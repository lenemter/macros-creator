from typing import Iterable


def write_file_xml(filepath, actions: Iterable, settings: dict):
    import xml.etree.ElementTree as ElementTree
    import xml.dom.minidom as minidom

    settings = {str(x): str(y) for (x, y) in settings.items()}

    root = ElementTree.Element('macro', settings)
    for action in actions:
        root.append(action.xml())

    # prettify
    rough_string = ElementTree.tostring(root, 'UTF-8', method='xml')
    parsed = minidom.parseString(rough_string)
    parsed = parsed.toprettyxml(indent='\t', encoding='UTF-8')

    with open(filepath, mode='wb') as file:
        file.write(parsed)


def write_file_csv(filepath, actions: Iterable, settings: dict):
    import csv
    from .utils import DELIMITER, QUOTECHAR, QUOTE_METHOD

    with open(filepath, mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTE_METHOD)
        writer.writerow(['macro'] +
                        [f'{setting}={value}' for (setting, value) in settings.items()])

        for action in actions:
            writer.writerow([action.xml_name] +
                            [f'{parameter}={value}' for (parameter, value) in
                             action.parameters.items()])


def write_file_db(filepath, actions: Iterable, settings: dict):
    from io import StringIO
    import csv
    import sqlite3
    from .utils import DELIMITER, QUOTECHAR, QUOTE_METHOD

    # create csv string
    settings_data = StringIO()
    writer = csv.writer(settings_data, delimiter=DELIMITER,
                        quotechar=QUOTECHAR, quoting=QUOTE_METHOD)
    writer.writerow(['macro'] +
                    [f'{setting}={value}' for (setting, value) in settings.items()])

    for action in actions:
        writer.writerow([action.xml_name] +
                        [f'{parameter}={value}' for (parameter, value) in
                         action.parameters.items()])

    settings_data = [x.strip() for x in settings_data.getvalue().split('\n') if x]

    # connect to db and write csv
    connection = sqlite3.connect(filepath)
    cursor = connection.cursor()
    cursor.execute("""
                    DROP TABLE IF EXISTS settings
                    """)
    cursor.execute("""
                    DROP TABLE IF EXISTS macro
                   """)

    cursor.execute("""
                    CREATE TABLE settings (
                        id INTEGER PRIMARY KEY,
                        settings TEXT
                    )
                    """)
    cursor.execute("""
                    CREATE TABLE macro (
                        id INTEGER PRIMARY KEY,
                        action TEXT
                    )
                   """)
    cursor.execute(f"""
                    INSERT INTO settings (settings)
                    VALUES ('{settings_data[0]}')
                    """)
    for line in settings_data[1:]:
        cursor.execute(f"""
                        INSERT INTO macro (action)
                        VALUES ('{line}')
                        """)

    connection.commit()
    connection.close()

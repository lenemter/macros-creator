from .utils import NAME_CLASS_DICT


def write_file_xml(filepath, actions_list: list, settings: dict):
    import xml.etree.ElementTree as ET

    settings = {str(x): str(y) for (x, y) in settings.items()}

    root = ET.Element('macro', settings)
    for action in actions_list:
        root.append(action.xml())
    tree = ET.ElementTree(root)
    with open(filepath, mode='wb') as file:
        tree.write(file, encoding='UTF-8')


def write_file_db(filepath, actions_list: list, settings: dict):
    import sqlite3

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
                        name TEXT PRIMARY KEY,
                        value TEXT
                    )
                    """)
    cursor.execute("""
                    CREATE TABLE macro (
                        name TEXT PRIMARY KEY,
                        parameters TEXT
                    )
                   """)

    for (setting, value) in settings.items():
        cursor.execute(f"""
                        INSERT INTO settings (name, value)
                        VALUES ("{setting}", "{value}")
                        """)
    for action in actions_list:
        name = NAME_CLASS_DICT[action.name].__name__
        cursor.execute(f"""
                        INSERT INTO macro (name, parameters)
                        VALUES ("{name}", "{str(action.parameters)[1:-1]}")
                        """)

    connection.commit()
    connection.close()

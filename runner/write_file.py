from .utils import NAME_CLASS_DICT


def write_file_xml(filepath, actions: list, settings: dict):
    import xml.etree.ElementTree as ET

    settings = {str(x): str(y) for (x, y) in settings.items()}

    root = ET.Element('macro', settings)
    for action in actions:
        root.append(action.xml())
    tree = ET.ElementTree(root)
    with open(filepath, mode='wb') as file:
        tree.write(file, encoding='UTF-8')

def write_file_csv(filepath, actions: list, settings: dict):
    pass
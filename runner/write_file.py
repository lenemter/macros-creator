from typing import Iterable


def write_file_xml(filepath, actions: Iterable, settings: dict):
    import xml.etree.ElementTree as ElementTree
    import xml.dom.minidom as minidom

    settings = {str(x): str(y) for (x, y) in settings.items()}

    root = ElementTree.Element('macro', settings)
    for action in actions:
        root.append(action.xml())

    # prettify XML
    rough_string = ElementTree.tostring(root, 'UTF-8', method='xml')
    parsed = minidom.parseString(rough_string)
    parsed = parsed.toprettyxml(indent='\t', encoding='UTF-8')

    with open(filepath, mode='wb') as file:
        file.write(parsed)

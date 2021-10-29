def write_file_xml(filepath, actions: list, settings: dict):
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


def write_file_csv(filepath, actions: list, settings: dict):
    import csv
    from .utils import DELIMITER, QUOTECHAR, QUOTE_METHOD

    with open(filepath, mode='w', encoding='UTF-8') as file:
        writer = csv.writer(file, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=QUOTE_METHOD)
        writer.writerow(['marco'] +
                        [f'{setting}={value}' for (setting, value) in settings.items()])

        for action in actions:
            writer.writerow([action.xml_name] +
                            [f'{parameter}={value}' for (parameter, value) in action.parameters.items()])

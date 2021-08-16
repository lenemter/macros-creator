import xml.etree.ElementTree as ET


def write_file(path, actions):
    root = ET.Element('macro')
    for action in actions:
        root.append(action.xml())
    tree = ET.ElementTree(root)
    tree.write(path)

from actions.Action import Action
import xml.etree.ElementTree as ET

name_class_dict = dict()
for cls in Action.__subclasses__():
    name_class_dict[cls.name] = cls


def read_file(filepath) -> list:
    actions = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    for child in list(root):
        child: ET.Element = child
        tag = child.tag
        attrib = child.attrib
        action = name_class_dict[tag.capitalize().replace('_', ' ')](**attrib)
        actions.append(action)
    return actions

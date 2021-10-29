import csv

import actions

NAME_CLASS_DICT = {_cls.name: _cls for _cls in actions.Action.__subclasses__()}

# CSV
DELIMITER = ';'
QUOTECHAR = '"'
QUOTE_METHOD = csv.QUOTE_ALL

from time import sleep

from parser.FileRead import read_file


def run(filepath):
    sleep(1)
    actions = read_file(filepath)
    for action in actions:
        action.run()

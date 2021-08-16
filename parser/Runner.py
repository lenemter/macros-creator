from time import sleep

from parser.FileRead import read_file


def run(filepath):
    sleep(1)
    actions = read_file(filepath)
    i = 0
    while i < len(actions):
        next_line = actions[i].run()
        if next_line is None:
            next_line = i + 1
        else:
            next_line -= 1  # Convert line to index
        i = next_line

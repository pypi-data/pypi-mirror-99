import json


def parse_files(path):
    return json.load(open(path, 'r'))

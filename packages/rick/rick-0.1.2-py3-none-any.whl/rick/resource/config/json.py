import json

from rick.base import ShallowContainer


def json_file(filename: str) -> ShallowContainer:
    try:
        with open(filename) as cfg_file:
            contents = json.loads(cfg_file.read())
    except IOError as e:
        raise RuntimeError("an exception occurred when loading config file {}: {}".format(filename, str(e)))

    return ShallowContainer(contents)

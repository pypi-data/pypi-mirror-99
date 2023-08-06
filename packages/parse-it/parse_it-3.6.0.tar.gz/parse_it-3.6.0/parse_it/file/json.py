from parse_it.file.file_reader import *
import json


def parse_json_file(path_to_json_file: str) -> dict:
    """take a path to a JSON file & returns it as a valid python dict.

            Arguments:
                path_to_json_file -- the path of the json file
            Returns:
                config_file_dict -- dict of the file
    """
    return json.loads(read_file(path_to_json_file))

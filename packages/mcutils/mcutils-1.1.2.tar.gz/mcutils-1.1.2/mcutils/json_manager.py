import json


def get_dict_from_json(path):
    """
    Loads json file as dict

    Args:
        path (str): path of the json file to load
    """
    with open(path, "r") as json_file:
        dictionary = json.load(json_file)
    return dictionary


def generate_json(path, dictionary):
    """
    Writes dict as json

    Args:
        path (str): path to write the json file
        dictionary (dict): dict to write as json
    """
    with open(path, "w") as json_file:
        json.dump(dictionary, json_file)

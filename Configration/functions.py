import json

import os


def load_train_config():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(root_dir, 'config.json')
    with open(config_path) as json_data_file:
        data = json.load(json_data_file)
    return data["train"]


def load_neural_config():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(root_dir, 'config.json')
    with open(config_path) as json_data_file:
        data = json.load(json_data_file)
    return data["neural"]


def load_data_generator_config():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(root_dir, 'config.json')
    with open(config_path) as json_data_file:
        data = json.load(json_data_file)
    return data["data_generator"]

import pathlib 
import yaml
from typing import Dict

def load_yaml(path : pathlib.Path = None)->Dict:
    """
    yamlfileを読み込む
    """
    assert pathlib.Path.exists(path), "There is not .pashea.yaml"

    with open(path, "r") as y:
        default = yaml.safe_load(y)

    return default

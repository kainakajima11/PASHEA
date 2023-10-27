import pathlib 
import yaml
from typing import List, Dict, Final

DOT_PATH : Final[pathlib.Path] = pathlib.Path.home() / ".pashea.yaml"
DEFAULT : Final[Dict] = {}

PARA : Final[List[str]] = None

CRACK_DEPTH : Final[float] = None
CRACK_ANGLE : Final[float] = None
EMPTY_LENGTH : Final[float] = None

def load_yaml(path : pathlib.Path = None)->Dict:
    """
    yamlfileを読み込む
    """
    with open(path, "r") as y:
        default = yaml.safe_load(y)
    return default

def set_default():
    """
    ~/.pashea.yaml から default値を設定する.
    """
    if not pathlib.Path.exists(DOT_PATH):
        print("NO DEFAULT")
        return

    global DEFAULT
    DEFAULT = load_yaml(DOT_PATH)

    if "PARA" in DEFAULT:
        global PARA
        PARA = DEFAULT["PARA"] 
    
    if "CRACK_DEPTH" in DEFAULT:
        global CRACK_DEPTH
        CRACK_DEPTH = DEFAULT["CRACK_DEPTH"] 
    
    if "CRACK_ANGLE" in DEFAULT:
        global CRACK_ANGLE
        CRACK_ANGLE = DEFAULT["CRACK_ANGLE"] 

    if "EMPTY_LENGTH" in DEFAULT:
        global EMPTY_LENGTH
        EMPTY_LENGTH = DEFAULT["EMPTY_LENGTH"] 

#! /usr/bin/env python3
import argparse
import pathlib
import pandas as pd
import numpy as np
from typing import List
from pashea import AlloyAnalyzer
"""
粒界モデルを作成する.
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    aa = AlloyAnalyzer()
    aa.makeGBModel()
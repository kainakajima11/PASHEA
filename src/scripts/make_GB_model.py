#! /usr/bin/env python3
import argparse
import pathlib
import pandas as pd
import numpy as np
from typing import List
from pashea import AnalizeHEA
from pashea import Default as D
"""
粒界モデルを作成する.
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    if pathlib.Path.exists(D.DOT_PATH):
        D.set_default()

    parser = argparse.ArgumentParser(
        description = "粒界モデルを作成する"
    )
    parser.add_argument("-p", "--para", default=None, type=List[str],
                        help = "para")
    parser.add_argument("-d", "--crack_depth", default=None, type=float,
                        help = "crack_depth")
    parser.add_argument("-a", "--crack_angle", default=None, type=float,
                        help = "crack_angle")
    parser.add_argument("-e", "--empty_length", default=None, type=float,
                        help = "empty_length")
    args = parser.parse_args()

    crack_angle = args.crack_angle
    if crack_angle is None:
        crack_angle = D.CRACK_ANGLE

    crack_depth = args.crack_depth
    if crack_depth is None:
        crack_depth = D.CRACK_ANGLE
    
    empty_length = args.empty_length
    if empty_length is None:
        empty_length = D.EMPTY_LENGTH

    carfile_path = input("carfile_path\n")
    replicate_num = list(map(int,input("replicate_num\n").split()))
    type_ratio = list(map(int,input("type_ratio\n").split()))
    lattice_const = list(map(float,input("lattice_const\n").split()))
    output_file = input("output_file_path\n")

    ahea = AnalizeHEA()
    ahea.MakeGBModel(
        carfile_path = carfile_path,
        replicate_num = replicate_num,
        crack_depth = crack_depth,
        crack_angle = crack_angle,
        output_file = output_file,
        para = args.para,
        type_ratio = type_ratio,
        empty_length = empty_length,
        lattice_const = lattice_const,
    )
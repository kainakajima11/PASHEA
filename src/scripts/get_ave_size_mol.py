#! /usr/bin/env python3
import argparse
import pathlib
import numpy as np
import pandas as pd
from limda import SimulationFrames
from pashea import AlloyAnalyzer

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "分子の平均サイズを知る"
    )
    parser.add_argument("target_file", help="lammpsdumpposファイル,分子ごとに分かれている", type=str)
    parser.add_argument("-s","--start_i", default=None, help="lammpsdumpposファイル,分子ごとに分かれている", type=int)
    parser.add_argument("-e","--end_i", default=None, help="lammpsdumpposファイル,分子ごとに分かれている", type=int)
    args = parser.parse_args()
    sfs = SimulationFrames()
    sfs.import_lammps_dumpposes(args.target_file)
    if args.start_i is None:
        args.start_i = 0
    if args.end_i is None:
        args.end_i = len(sfs.sf)
    assert 0 <= args.start_i and args.start_i < args.end_i and args.end_i <= len(sfs.sf)
    ave_size = 0
    for i in range(args.start_i, args.end_i):
        ave_size += len(sfs.sf[i])
    ave_size /= len(sfs.sf) - 1
    print(ave_size)
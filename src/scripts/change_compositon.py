#! /usr/bin/env python3
import argparse
from copy import deepcopy
import numpy as np
import pandas as pd
from limda import SimulationFrame
from pashea import AlloyAnalyzer

"""
dump.pos fileが存在するdirに対して、
構造を読み込み、酸化物にだけにする（水中に浮き出したものも）
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "組成を変更する"
    )
    parser.add_argument("target_file", help="inputfile", type=str)
    parser.add_argument("output_file", help="outputfile", type=str)
    parser.add_argument("-b", "--before_types", nargs='+', help="b", type=int)
    parser.add_argument("-a", "--after_types", nargs='+', help="b", type=int)
    parser.add_argument("-c", "--change_nums", nargs='+', help="b", type=int)

    args = parser.parse_args()
    l = len(args.before_types)
    assert l == len(args.after_types) and l == len(args.change_nums)
    sf = SimulationFrame()
    sf.import_file(args.target_file)
    csf = deepcopy(sf)

    for i in range(len(args.before_types)):
        indices = csf.atoms[csf.atoms["type"] == args.before_types[i]].index
        indices = np.random.permutation(indices)
        for j in range(args.change_nums[i]):
            sf.atoms.loc[indices[j], "type"] = args.after_types[i]

    sf.export_file(args.output_file)
    sf.export_dumppos("ch_comp.pos")


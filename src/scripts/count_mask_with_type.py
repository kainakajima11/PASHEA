#! /usr/bin/env python3
import argparse
import pathlib
import numpy as np
import pandas as pd
from limda import SimulationFrame
from pashea import AlloyAnalyzer

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "maskとtypeで分けて原子数を数える"
    )
    parser.add_argument("target_file", help="inputファイル", type=str)
    args = parser.parse_args()

    sf = SimulationFrame()
    sf.import_file(args.target_file)
    l_type = len(sf.atom_symbol_to_type)
    mask_max = np.max(sf.atoms["mask"].values)
    mask_and_type = [
            [0 for _ in range(mask_max + 1)] for __ in range(l_type)
    ]

    for i in range(len(sf)):
        t = sf.atoms["type"][i] 
        m = sf.atoms["mask"][i]
        mask_and_type[t-1][m] += 1

    for i in range(l_type):
        print(*mask_and_type[i])

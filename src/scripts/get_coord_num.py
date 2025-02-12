#! /usr/bin/env python3
import argparse
import numpy as np
import pandas as pd
from limda import SimulationFrame
from pashea import AlloyAnalyzer

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "各タイプの原子の配位数（酸素）を知る"
    )
    parser.add_argument("target_file", help="dumpposファイル", type=str)
    args = parser.parse_args()

    sf = SimulationFrame()
    sf.import_dumppos(args.target_file)
    neighbor_list = sf.get_neighbor_list(mode="bond_length")
    max_coord = 0
    n_type = len(sf.atom_symbol_to_type)
    coords = [
        [0 for _ in range(100)] for __ in range(n_type)
    ]
    for i in range(len(sf)):
        type_i = sf.atoms["type"][i]
        if type_i <= 5 or type_i == 8:
            coord = 0
            for j in neighbor_list[i]:
                if sf.atoms["type"][j] == 7:
                    coord += 1
            max_coord = max(coord, max_coord)
            coords[type_i - 1][coord] += 1

    for i in range(n_type):
        for j in range(1,max_coord+1):
            print(coords[i][j], end=" ")
        print()
#! /usr/bin/env python3
import argparse
import numpy as np
import pandas as pd
from limda import SimulationFrame
from pashea import AlloyAnalyzer

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "酸化物内のOを分類する"
    )
    parser.add_argument("target_file", help="dumpposファイル", type=str)
    args = parser.parse_args()

    sf = SimulationFrame()
    sf.import_dumppos(args.target_file)
    oxygen_type = np.array([0 for _ in range(len(sf))]) # 0:metal, 1 ~ : oxygen
    is_termial_oxygen = np.array([0 for _ in range(len(sf))])
    neighbor_list = sf.get_neighbor_list(mode="bond_length")
    for i in range(len(sf)):
        type_i = sf.atoms["type"][i]
        if type_i != 7:
            continue
        metal_n = 0
        hyd_n = 0 
        for j in neighbor_list[i]:
            type_j = sf.atoms["type"][j]
            if type_j != 6 and type_j != 7:
                metal_n += 1
            elif type_j == 6:
                hyd_n += 1
        if metal_n == 1:
            is_termial_oxygen[i] = 1
        oxygen_type[i] = hyd_n + 1

    categories = [
        {} for _ in range(len(sf.atom_symbol_to_type))
    ]
    for i in range(len(sf)):
        type_i = sf.atoms["type"][i]
        if type_i == 6 or type_i == 7:
            continue
        for j in neighbor_list[i]:
            type_j = sf.atoms["type"][j]
            if type_j != 7:
                continue
            key = oxygen_type[j]
            if is_termial_oxygen[j]:
                key *= -1
            categories[type_i - 1][key] = categories[type_i - 1].get(key, 0) + 1

    for i in range(len(sf.atom_symbol_to_type)):
        if i + 1 != 6 and i + 1 != 7:
            keys = sorted(categories[i].keys())
            for key in keys:
                print(f"{key}:{categories[i][key]}", end=" ")
            print()

"""
keyが正 -> 終端ではない、他の金属と接する
keyが負 -> 終端
keyの絶対値 - 1, 酸素と結合をもつ水素の数 
"""


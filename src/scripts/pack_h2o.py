#! /usr/bin/env python3
import argparse
import pathlib
import numpy as np
import pandas as pd
from limda import SimulationFrames
from pashea import AlloyAnalyzer
from limda import SimulationFrame

"""
dump.pos fileが存在するdirに対して、
構造を読み込み、合金表面の酸化物以外の原子を削除する
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "H2Oを詰める"
    )

    parser.add_argument("input_file", help="input file", type=str)
    parser.add_argument("output_file", help="output file", type=str)
    parser.add_argument("-y","--y_min", default=74, help="y_min", type=float)
    parser.add_argument("-n", "--num_h2o", default=3000, type=float)
    args = parser.parse_args()

    sf = SimulationFrame()
    sf.import_file(args.input_file)
    sf_h2o = SimulationFrame()
    sf_h2o.import_mol("H2O")
    alloy_y_mx = sf.atoms["y"].max()
    alloy_y_mn = sf.atoms["y"].min()
    sf.atoms["y"] -= alloy_y_mn - 0.000001
    xyz_condition = [
            [0.5, args.y_min,  0.5, sf.cell[0]-0.5, sf.cell[1]-2.0, sf.cell[2]-0.5],
    ]
    sf.packmol(sf_list=[sf_h2o],
                pack_num_list=[args.num_h2o],
                tolerance = 1.8,
                xyz_condition = xyz_condition,
                print_packmol=True,
                seed=-1)
    sf.export_input(args.output_file)
    sf.export_dumppos("packdump.pos")
    
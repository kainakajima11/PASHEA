#! /usr/bin/env python3
import argparse
import pathlib
import numpy as np
import pandas as pd
from limda import SimulationFrames
from pashea import AlloyAnalyzer
import copy

"""
dump.pos fileが存在するdirに対して、
構造を読み込み、合金表面の酸化物以外の原子を削除する
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "金表面の酸化物以外の原子を削除する"
    )
    parser.add_argument("target_dir", help="dumpposファイルがあるフォルダ", type=str)
    parser.add_argument("output_dir", help="dumpposファイルを出力するフォルダ", type=str)
    parser.add_argument("-s", "--skip_num", help="skip_num", type=int, default=1)
    parser.add_argument('-alloy', '--flag_out_alloy', action='store_true')
    parser.add_argument("-no_surface", "--flag_no_surface", help="store_true")
    args = parser.parse_args()
    args.target_dir = pathlib.Path(args.target_dir).resolve()
    args.output_dir = pathlib.Path(args.output_dir).resolve()
    if args.flag_out_alloy:
        print("OUTPUT ONLY ALLOY STRUCTURES")
    if not args.flag_no_surface:
        print("OUTPUT ONLY SURFACE STRUCTURES")
    sfs = SimulationFrames()
    bond_length = sfs.limda_default["bond_length"]
    bond_length_metal = bond_length.copy()
    for i in range(8):
        for j in range(8):
            if (i+1 <= 5 or i+1 == 8) and (j+1 <= 5 or j+1 == 8):
                bond_length_metal[i][j] = 2.5
    sfs.import_dumpposes(args.target_dir, skip_num=args.skip_num)
    for i, sf in enumerate(sfs.sf):
        remain = np.array([False for _ in range(len(sf))])
        mols_list = sf.get_mols_list(bond_length=bond_length_metal)
        for l in mols_list:
            if len(l) > 1000:
                for id in l:
                    remain[id] = True

        sf.atoms = sf.atoms[remain]
        sf.atoms = sf.atoms.reset_index()
        if args.flag_out_alloy:
            sf.export_dumppos(f"{args.output_dir}/alloy.pos.{sf.step_num}")  

        remain = np.array([False for _ in range(len(sf))])
        mols_list = sf.get_mols_list(bond_length=bond_length)
        for l in mols_list:
            if len(l) == 1:
                continue
            for id in l:
                remain[id] = True
        sf.atoms = sf.atoms[remain]
        sf.atoms = sf.atoms.reset_index()
        if len(sf) > 0 and not args.flag_no_surface:
            sf.export_dumppos(f"{args.output_dir}/dump.pos.{sf.step_num}")

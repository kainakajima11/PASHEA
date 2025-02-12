#! /usr/bin/env python3
import argparse
import pathlib
import pandas as pd
import numpy as np
from copy import deepcopy
from limda import SimulationFrame, SimulationFrames

"""
seperate_by_mols.py dump.pos.500
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = ""
    )
    parser.add_argument("input_file", help="dumpposファイルのパス", type=str)
    parser.add_argument("-o", "--output_file", default="mols.pos", help="出力するlammps_dumpposファイル", type=str)
    args = parser.parse_args()

    sf = SimulationFrame()
    sf.import_file(args.input_file)
    sf_mol = deepcopy(sf)
    mols_list = sf.get_mols_list()
    idx_mol = 1
    for l in mols_list:
        if len(l) == 1:
            continue
        for id in l:
            sf.atoms.loc[id, "mask"] = idx_mol
        idx_mol += 1
    print(sf.atoms)
    sfs = SimulationFrames()
    sfs.sf.append(sf)
    for i in range(1, idx_mol):
        sf_mol.atoms = sf.atoms.loc[sf.atoms["mask"] == i]
        sfs.sf.append(deepcopy(sf_mol))
    sfs.sf = sorted(sfs.sf, key=len, reverse=True)
    sfs.export_lammps_dumpposes(f"{args.output_file}")

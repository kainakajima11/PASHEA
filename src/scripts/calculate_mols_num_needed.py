#! /usr/bin/env python3
import argparse
import pathlib
import pandas as pd
from pashea import AlloyAnalyzer

"""
指定分子を何個入れたら指定密度になるかを出力する
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "分子を指定密度にするために何個必要か出力する"
    )
    parser.add_argument("-i", "--input_file_path", default=None, type=str,
                        help = "input file path")

    args = parser.parse_args()
    args.input_file_path = pathlib.Path(args.input_file_path).resolve()
    aa.sf.import_file(args.input_file_path)
    print(f"Type Ratio : {aa.getFrameTypeRatio()}")
    alloy_density = aa.calculateAlloyDensity(
        lattice_const = aa.D["calculateAlloyDensity"]["lattice_const"],
        type_ratio = aa.getFrameTypeRatio(),
        crystal_type = aa.D["calculateAlloyDensity"]["crystal_type"],
    ) 
    print(f'This {aa.D["calculateAlloyDensity"]["crystal_type"]} alloys density is {alloy_density} g/cm^3')
    mols_num_needed = aa.calculateMolsNumNeeded(
        alloy_density = alloy_density,
        aim_density = aa.D["calculateMolsNumNeeded"]["aim_density"],
        init_mol = aa.D["calculateMolsNumNeeded"]["init_mol"]
    )
    print(f"Mols number needed : {mols_num_needed}")
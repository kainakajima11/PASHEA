#! /usr/bin/env python3
import argparse
import pathlib
import pandas as pd
import numpy as np
from typing import List
from pashea import AlloyAnalyzer
"""
input fileにstrainの行を加える
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "input.rdにstrainの情報を加える(z only)"
    )
    parser.add_argument("-i", "--input_file", default=aa.D["addStrainLine"]["input_file_path"], type=str,
                        help = "input_file_path")
    parser.add_argument("-v", "--strain_velocity", default=aa.D["addStrainLine"]["strain_velocity"], type=float,
                        help = "strain_velocity")
    args = parser.parse_args()

    assert args.input_file is not None

    strain_lines = f"#strain - - - - z {args.strain_velocity}\n"
    insert_line_id = 0
    with open(args.input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            insert_line_id += 1
            if len(line.split()) == 0:
                continue
            if line.split()[0] == "#cellx":
                strain_lines += line.split()[2]
                strain_lines += " "
            elif line.split()[0] == "#celly":
                strain_lines += line.split()[2]
                strain_lines += " "
            elif line.split()[0] == "#cellz":
                strain_lines += line.split()[2]
                strain_lines += "\n"
                break
    lines.insert(insert_line_id, strain_lines)
    with open(args.input_file, "w") as f:
        f.writelines(lines)

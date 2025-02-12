#! /usr/bin/env python3
from limda import SimulationFrame
import pandas as pd
import argparse
import numpy as np

pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="原子の数を原子種ごとにカウントする")
    parser.add_argument(
        "-i", "--input_file_name", default=None, type=str, help="対象のファイル名"
    )

    args = parser.parse_args()

    assert args.input_file_name is not None, "file_nameを設定してください"

    sf = SimulationFrame()
    sf.import_file(args.input_file_name)
    max_mask = np.max(sf.atoms["mask"])
    cnts = [0 for _ in range(max_mask + 1)]
    for i in range(max_mask + 1):
        df = sf.atoms.loc[sf.atoms["mask"] == i]
        cnts[i] = len(df)
    print(*cnts)
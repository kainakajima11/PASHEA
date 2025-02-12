#! /usr/bin/env python3
import argparse
import pathlib
import numpy as np
import pandas as pd
from limda import SimulationFrames

"""
dump.pos fileが存在するdirに対して、
構造を読み込み、酸化物にだけにする（水中に浮き出したものも）

delete_expect_oxide.py . Oxide -s 10

"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "酸化物以外を除去する"
    )
    parser.add_argument("target_dir", help="dumpposファイルがあるフォルダ", type=str)
    parser.add_argument("output_dir", help="dumpposファイルを出力するフォルダ", type=str)
    parser.add_argument("-s", "--skip_num", help="skip_num", type=int, default=1)
    args = parser.parse_args()
    args.target_dir = pathlib.Path(args.target_dir).resolve()
    args.output_dir = pathlib.Path(args.output_dir).resolve()

    sfs = SimulationFrames()
    sfs.import_dumpposes(args.target_dir, skip_num=args.skip_num)
    for i, sf in enumerate(sfs.sf):
        remain = np.array([False for _ in range(len(sf))])
        mols_list = sf.get_mols_list()
        for l in mols_list:
            if len(l) == 1:
                continue
            m_o_flag = 0
            for id in l:
                if sf.atoms["type"][id] <= 5 or sf.atoms["type"][id] == 8: # metal condition 
                    m_o_flag |= 1<<0
                elif sf.atoms["type"][id] == 7: # oxygen condition
                    m_o_flag |= 1<<1 
            if m_o_flag == (1<<2) - 1:
                for id in l:
                    remain[id] = True

        sf.atoms = sf.atoms[remain]
        sf.atoms = sf.atoms.reset_index()
        sf.atoms["y"] += 0.7 * sf.cell[1] # slide atoms
        sf.wrap_atoms()
        sf.export_dumppos(f"{args.output_dir}/dump.pos.{sf.step_num}")

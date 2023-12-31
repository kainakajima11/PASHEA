#! /usr/bin/env python3
import argparse
import pathlib
import pandas as pd
from pashea import AlloyAnalyzer

"""
ovitoで相の割合をテキストファイルとして出力すると、
テキストファイルがstep数だけできるので、それらをひとまとめにして
pandasのDataframeとして扱いやすい形で出力する。
"""
pd.set_option("display.max_rows", None)

if __name__ == "__main__":
    aa = AlloyAnalyzer()

    parser = argparse.ArgumentParser(
        description = "Ovitoから得た,相割合のファイル群をcsv fileとしてひとまとめにする。"
    )
    parser.add_argument("-i", "--input_dir", default=aa.D["consolidatePhaseRatioFile"]["input_dir"], type=str,
                        help = "相割合のfileが入った、ディレクトリ")
    parser.add_argument("-n", "--filename", default=aa.D["consolidatePhaseRatioFile"]["input_filename"], type=str,
                        help = "相割合のfileの名前 ({file_name}.idx)")
    parser.add_argument("-o", "--output_dir", default=aa.D["consolidatePhaseRatioFile"]["output_dir"], type=str,
                        help = "出力するディレクトリ")
    parser.add_argument("-c", "--csv_filename", default=aa.D["consolidatePhaseRatioFile"]["csv_filename"], type=str,
                        help = "出力するcsvファイルの名前")

    args = parser.parse_args()

    assert not args.filename.isdigit(), "Sorry, this program is Not adapted to filename with numbers in it."

    args.input_dir = pathlib.Path(args.input_dir).resolve()
    args.output_dir = pathlib.Path(args.output_dir).resolve()
    aa.consolidatePhaseRatioFile(
        input_dir = args.input_dir,
        filename = args.filename, 
        output_dir = args.output_dir,
        csv_filename = args.csv_filename,
    ) 
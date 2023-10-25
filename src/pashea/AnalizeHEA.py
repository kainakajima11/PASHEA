import numpy as np
from numpy.typing import ArrayLike
import pandas as pd
import pathlib
from typing import Dict, List, Union

class AnalizeHEA:
    def __init__(self):
        pass

    def consolidate_phase_ratio_file(
        self,
        input_dir : Union[str, pathlib.Path] = None,
        filename : str = "phase_ratio",
        output_dir : Union[str, pathlib.Path] = None,
        csv_filename : str = "PhaseRatio",
    ):
        """
        合計原子数と各ステップのそれぞれの相の原子数の情報が入ったファイルを出力する。
        
        Arguments
        ---------
            input_dir : Union[str, pathlib.Path]
                読み込むファイルが入ったディレクトリ
            filename : str
                input_dir内の読み込みたいファイルの名前
                (実際のファイル名は filename + ".i")
            output_dir : Union[str, pathlib.Path]
                ファイルを出力する場所
            csv_filename : str
                出力するファイル名

        ex.
        outputfileの中身
        -----------------------
        AtomNum 10000 
        
        Step Other FCC HCP BCC
        1 1000 3000 3000 3000
        .
        .
        .
        1000 2000 8000 0 0
        -----------------------
        """
        files = list(input_dir.glob(f"{filename}.*"))
        AtomNum = 0
        Phase : Dict[str, ArrayLike] = {}
        Phase["Step"] = np.empty(len(files), dtype=np.int32)

        # get atom numbers and initialize arrays
        with open(files[0], "r") as f:
            lines = f.readlines()
            for line in lines:
                spline = line.split()
                if spline[0] == "#":
                    continue
                Phase[spline[0]] = np.zeros(len(files), dtype=np.int32)
                AtomNum += int(spline[1])

        # extract data from each file
        for i, file in enumerate(files):
            step = ''.join(filter(str.isdigit, file.name))
            Phase["Step"][i] = np.int32(step)
            with open(file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    spline = line.split()
                    if spline[0] == "#":
                        continue
                    Phase[spline[0]][i] = np.int32(spline[1])

        PhaseDf = pd.DataFrame(Phase)
        PhaseDf = PhaseDf.sort_values(by='Step')

        # consolidate files
        with open(output_dir / csv_filename, "w") as f:
            f.write(f"AtomNum {AtomNum}\n\n")
        PhaseDf.to_csv(output_dir / csv_filename, sep=' ', mode='a', index=False)           
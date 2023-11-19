import numpy as np
from numpy.typing import ArrayLike
import pandas as pd
import pathlib
from typing import Dict, List, Union, Any
from limda import SimulationFrame
from .Default import load_yaml, AVOGADORO_CONST

class AlloyAnalyzer:
    D : dict[str, Any]
    sf : SimulationFrame

    def __init__(self):
        self.D = load_yaml(pathlib.Path.home() / ".pashea.yaml")
        self.sf = SimulationFrame()

    def consolidatePhaseRatioFile(
        self,
        input_dir : Union[str, pathlib.Path] = None,
        filename : str = None,
        output_dir : Union[str, pathlib.Path] = None,
        csv_filename : str = None,
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

    def makeGBModel(self):
        """
        粒界モデルを作成する
        """
        d = self.D["makeGBModel"]
        self.sf.import_car(d["car_file_path"])
        self.sf.change_lattice_const(d["lattice_const"])
        self.sf.replicate_atoms(d["replicate_num"])
        self.make_precrack(d["crack_depth"], d["crack_angle"])
        self.sf.mirroring_atoms()
        segment_num = [max(1,sf.cell[0]//d["shuffle_segment"][0]), max(1,sf.cell[1]//d["shuffle_segment"][1]), max(1,sf.cell[2]//d["shuffle_segment"][1])]
        self.sf.shuffle_type_by_part(segment_num=segment_num,
                                     type_ratio=d["type_ratio"])
        self.sf.make_empty_space(empty_length=d["empty_length"], direction = "y", both_direction = d["both_direction"])
        self.sf.slide_atoms([0.000001, 0.000001, 0.000001])
        self.sf.export_input(d["output_file_path"])
        self.sf.export_dumppos("showdump.pos")
        print(len(self.sf))
        print(self.sf.cell)

    def make_precrack(
        self,
        crack_depth,
        crack_angle
    ):
        crack_depth *= sf.cell[1]
        ax = np.array([])
        ay = np.array([])
        az = np.array([])
        for x, y, z in zip(sf.atoms["x"], sf.atoms["y"], sf.atoms["z"]):
            judge :bool = False
            if(y < sf.cell[1] - crack_depth):
                judge = True
            if(z > crack_angle * y - (sf.cell[1] - crack_depth) * crack_angle - 0.001):
                judge = True
            if judge:
                ax = np.append(ax, x)
                ay = np.append(ay, y)
                az = np.append(az, z)
        self.sf.atoms = pd.DataFrame({"type":np.ones(len(ax)), "x":ax, "y":ay, "z":az})
        
    def calculateAlloyDensity(self,
                              cell_size : ArrayLike = None,
                              type_ratio : ArrayLike = None,
                              crystal_type : str = "FCC"):
        """
        典型的な結晶タイプの金属の組成から密度を計算する.

        Auguments
        ---------
            cell_size : list[float]
                cell size [x,y,z]
            type_ratio : list[float]
                組成比, [type1, type2, ...]
            crystal_type : str
                結晶タイプ
        """
        atom_num = 0
        if crystal_type == "FCC":
            atom_num = 4
        elif crystal_type == "BCC":
            atom_num = 2
        else:
            raise ValueError("This crystal type is not supported.")
        ratio_sum = np.sum(type_ratio)
        mass_sum = np.sum(np.array([type_ratio[i]*self.sf.atom_type_to_mass[i+1] for i in range(len(type_ratio))]))
        volume = np.prod(cell_size) * (10 ** - 24)
        return atom_num * mass_sum / ratio_sum / volume / AVOGADORO_CONST 
            
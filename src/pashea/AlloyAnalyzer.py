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

    def get_volume(self):
        """
        sf.cell to volume (cm^3)
        """
        return np.prod(self.sf.cell) * (10 ** - 24)

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
        self.sf.mirroring_atoms()
        self.make_precrack(d["crack_depth"], d["crack_angle"], d["both_direction"])
        self.sf.shuffle_type(type_ratio=d["type_ratio"])
        self.sf.make_empty_space(empty_length=d["empty_length"], direction = "y", both_direction = False)
        self.sf.slide_atoms([0.000001, 0.000001, 0.000001])
        self.sf.export_input(d["output_file_path"])
        self.sf.export_dumppos("showdump.pos")
        print(len(self.sf))
        print(self.sf.cell)

    def make_precrack(
        self,
        crack_depth,
        crack_angle,
        both_direction,
    ):
        crack_depth *= self.sf.cell[1]

        class Line:
            def __init__(self, a, b):
                self.a = a
                self.b = b
            def get_online(self, x):
                return self.a * x + self.b
            
        def between_2_lines(u: Line, l: Line, x, y):
            return (l.get_online(x)  < y) & (y < u.get_online(x))
        
        is_in_crack = between_2_lines(
                Line(crack_angle, - (self.sf.cell[1] - crack_depth) * crack_angle + self.sf.cell[2]/2),
                Line(-crack_angle, (self.sf.cell[1] - crack_depth) * crack_angle + self.sf.cell[2]/2),
                self.sf.atoms["y"],
                self.sf.atoms["z"],
        )

        if both_direction:
            is_in_crack |= between_2_lines(
                Line(-crack_angle, crack_depth * crack_angle + self.sf.cell[2]/2),
                Line(crack_angle, - crack_depth * crack_angle + self.sf.cell[2]/2),
                self.sf.atoms["y"],
                self.sf.atoms["z"],
            )

        self.sf.delete_atoms(is_in_crack, reindex=True)

    def getFrameTypeRatio(self):
        """
        type_ratioをsfから作成
        """
        typs = self.sf.atoms["type"]
        type_ratio = [0 for i in range(len(self.sf.atom_type_to_mass))]
        for typ in typs:
            type_ratio[typ-1] += 1
        return type_ratio
           
    def calculateAlloyDensity(self,
                              lattice_const : ArrayLike = None,
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
        volume = np.prod(lattice_const) * (10 ** - 24)
        return atom_num * mass_sum / ratio_sum / volume / AVOGADORO_CONST 
        
    def calculateMolsNumNeeded(self,
                               alloy_density : float,
                               aim_density : float,
                               init_mol : ArrayLike) -> float:
        """
        指定分子を開いているスペースに何個入れたら、
        指定密度になるかを計算する.
        """
        overall_volume = self.get_volume()
        empty_space_volume = overall_volume - self.sf.density() * overall_volume / alloy_density
        sf_init_mol = SimulationFrame()
        sf_init_mol.cell = np.array([1.0,1.0,1.0])
        tmp_pos = [0 for i in range(len(init_mol))]
        sf_init_mol.atoms = pd.DataFrame({"type" : init_mol, "x":tmp_pos, "y":tmp_pos, "z":tmp_pos})
        mol_mass = sf_init_mol.density() * np.prod(sf_init_mol.cell) * (10 ** - 24)
        return aim_density * empty_space_volume / mol_mass
        

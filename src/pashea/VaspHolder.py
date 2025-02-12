from limda import SimulationFrame
from typing import Any
import pathlib
import yaml
import numpy as np

class VaspHolder:

    data : dict[str, Any]
    sf : SimulationFrame
    incar_config : dict[str, Any]
    iconst_config : list[str]

    def __init__(self):
        vasp_default_path = pathlib.Path.home() / ".my_vasp.yaml"
        if pathlib.Path.exists(vasp_default_path):
            with open(vasp_default_path, "r") as f:
                self.my_vasp = yaml.safe_load(f)
        else:
            self.my_vasp = {}
        self.incar_config = {}
        self.iconst_config = None

    def set_incar(self, incars : list[dict[str, Any]]):
        for incar in incars:
            self.incar_config.update(incar)

    def set_structure(self, frame):
        self.sf = frame.copy()
    

    # def set_vasp(self,
    #              magmom_set : bool = False):
    #     pass

    # def check_vasp(self,
    #                potim_check : bool = False,
    #                iconst_check : bool = False,
    #                cut_off_check : bool = False):
    #     if potim_check:
    #         self.check_potim()
    #     if iconst_check:
    #         self.check_iconst()
    #     if cut_off_check:
    #         self.check_cut_off()

    # def check_potim(self, ):
    #     if not "H" in self.sf.atom_symbol_to_type:
    #         return
    #     if self.sf.atom_symbol_to_type["H"] in self.sf.get_atom_type_set():
    #         self.incar_config["POTIM"] = 1.0

    # def check_iconst(self, ):
    #     if "PSTRESS" in self.incar_config:
    #         self.iconst_config = [ # 角度一定でNPTする設定 # NVTのときは消す
    #             'LA 1 2 0',
    #             'LA 1 3 0',
    #             'LA 2 3 0'
    #         ]

    # def check_cut_off(self, cut_off : 4.0):
    #     minimun_cell_length = cut_off * 2
    #     if np.min(self.sf.cell) < minimun_cell_length:
    #         return False
    #     else:
    #         return True
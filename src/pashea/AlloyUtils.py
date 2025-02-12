from limda import SimulationFrame
import numpy as np

class AlloyUtils:
    def __init__(self):
        pass

    def groupby_ll(ll: list[list], condition):
        """
        conditionに従って、listの大きさで二つにする
        ex.
        -- 合金成分か否かを得る（分子ごとに、サイズが10000以上かを得る）
        def condition(l: list):
            return len(l) >= 10000
        groupby_ll(sf.get_mols_list(), condition)
        """
        size_l = len(ll)
        trues = np.array([False for _ in range(size_l)])
        for l in ll:
            if condition(l):
                for id in l:
                    trues[id] = True
        return trues
    
    def groupby_with_a_type(sf: SimulationFrame, typ: int, ll: list[list] = None):
        """
        あるtypeの原子（sf.atoms["type"]==typ)と結合を持っているか
        """
        size_sf = len(sf)
        trues = np.array([False for _ in range(size_sf)])
        for i, l in enumerate(ll):
            if sf.atoms["type"][i] == typ:
                for j in l:
                    trues[j] = True
        return trues

            


        

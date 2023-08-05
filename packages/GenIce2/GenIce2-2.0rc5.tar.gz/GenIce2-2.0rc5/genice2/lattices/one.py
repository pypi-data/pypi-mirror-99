# coding: utf-8
desc={"ref": {},
      "usage": 'genice one[hcchchcc]; Specify layer types with "c" or "h".',
      "brief": "Ice I w/ stacking faults."
      }

import logging
import numpy as np
from genice2.cell import cellvectors
import genice2.lattices


lat = [[[0,0], [2,0], [1,3], [3,3]],
       [[0,2], [2,2], [1,5], [3,5]],
       [[0,4], [2,4], [1,1], [3,1]]]


class Lattice(genice2.lattices.Lattice):
    def __init__(self, **kwargs):
        logger = logging.getLogger()
        for k, v in kwargs.items():
            if k == 'layers':
                arg = v
            elif v == True: # in case only the char string is given
                arg = k
            else:
                logger.error(f"Unknown option for one plugin: {k}={v}")
        layer = 0
        height = 0
        dir = 1
        L = []
        for ch in arg:
            for x,y in lat[layer]:
                L.append([x, y, height])
            layer = (layer+dir+3) % 3
            height += 1
            for x,y in lat[layer]:
                L.append([x, y, height])
            height += 3
            assert ch in "CcHh"
            if ch in "Hh":
                # hexagonal = alternative
                dir = -dir
                #cubic = progressive
        assert layer == 0 and dir == 1, "Incompatible number of layers."
        self.waters = np.array(L) / np.array([4.0, 6.0, height])
        self.coord = "relative"
        LHB = 0.276
        self.bondlen = 0.3
        y = LHB* (8**0.5 / 3)*3
        x = y * 2 / 3**0.5
        z = LHB*height/3
        self.cell = cellvectors(x,y,z)
        self.density=0.92

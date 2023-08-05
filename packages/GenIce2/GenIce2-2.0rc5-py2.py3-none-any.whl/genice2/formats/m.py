# coding: utf-8

desc={"ref": {},
      "brief": "MDView file (in Angdtrom).",
      "usage": "No options available."
      }

if __name__[-6:] == 'mdv_au':
    desc["brief"] = "MDView file (in au)."

import numpy as np
from logging import getLogger
from genice2.decorators import timeit, banner
import genice2.formats


au = 0.052917721092 # nm
AA = 0.1 # nm


class Format(genice2.formats.Format):
    """
The atomic positions of the molecules are output in MDView format.
No options available.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def hooks(self):
        return {7:self.Hook7}


    @timeit
    @banner
    def Hook7(self, ice):
        "Output in MDView format."
        logger = getLogger()
        logger.info("  Total number of atoms: {0}".format(len(ice.atoms)))
        if __name__[-6:] == 'mdv_au':
            conv = 1.0 / au
        else:
            conv = 10.0
        cellmat = ice.repcell.mat
        s = ""
        s += "# {0} {1} {2}\n".format(cellmat[0,0]*conv, cellmat[1,1]*conv, cellmat[2,2]*conv)
        s += "-center 0 0 0\n"
        s += "-fold\n"
        s += "{0}\n".format(len(ice.atoms))
        for atom in ice.atoms:
            molorder, resname, atomname, position, order = atom
            s += "{0:5} {1:9.4f} {2:9.4f} {3:9.4f}\n".format(atomname,*(position[:3]*conv))
        self.output = s

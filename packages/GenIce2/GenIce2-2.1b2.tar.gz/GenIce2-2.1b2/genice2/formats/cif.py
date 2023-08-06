# coding: utf-8
"""
Crude Cif file format
"""

from math import acos,pi
import numpy as np
from logging import getLogger
from genice2.decorators import timeit, banner
import genice2.formats
from genice2.molecules  import serialize

def nearly_zero(x):
    return np.dot(x,x) < 1e-10


class Format(genice2.formats.Format):
    """
Atomic positions are in a crude CIF format.
No options available.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def hooks(self):
        return {7:self.Hook7}


    @timeit
    @banner
    def Hook7(self, ice):
        "Output in CIF format."
        logger = getLogger()
        aL, bL, cL, alpha, beta, gamma = ice.repcell.shape()
        s = ""
        s += "data_genice\n" # .format(ice.lattice_type)
        s += '#' + "\n#".join(ice.doc) + "\n"
        s += "_cell_length_a                {0}\n".format(aL*10)
        s += "_cell_length_b                {0}\n".format(bL*10)
        s += "_cell_length_c                {0}\n".format(cL*10)
        s += "_cell_angle_alpha             {0}\n".format(alpha)
        s += "_cell_angle_beta              {0}\n".format(beta)
        s += "_cell_angle_gamma             {0}\n".format(gamma)
        s += "\n"
        if nearly_zero(alpha-90) and nearly_zero(beta-90) and nearly_zero(gamma-90):
            s += "_symmetry_cell_setting        'orthorhombic'\n"
            s += "_symmetry_space_group_name_H-M   'P 1 '\n"
        else:
            s += "_symmetry_cell_setting        'triclinic'\n"  #for now it is always triclinic
            s += "_symmetry_space_group_name_H-M   'P 1 '\n"
        s += """
loop_
  _symmetry_equiv_pos_as_xyz
X,Y,Z

loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
"""
        atoms = []
        for mols in ice.universe:
            atoms += serialize(mols)

        for i, atom in enumerate(atoms):
            molorder, resname, atomname, position, order = atom
            position = ice.repcell.abs2rel(position)
            label = atomname+"{0}".format(i)
            s += "{4:>6}{0:>6}{1:10.4f}{2:10.4f}{3:10.4f}\n".format(atomname,position[0],position[1],position[2],label)
        s += "\n"
        self.output = s

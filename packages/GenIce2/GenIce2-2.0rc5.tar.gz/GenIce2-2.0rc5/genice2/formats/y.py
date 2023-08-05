# coding: utf-8

desc={"ref": {"Codes": "https://github.com/vitroid/Yaplot"},
      "brief": "Yaplot.",
      "usage": """
Usage: genice2 icename -f yaplot[options]

options:
    H=x   Set the radius of H to be x.
"""}


from collections import defaultdict
from logging import getLogger
import numpy as np
import yaplotlib as yp
from genice2.decorators import timeit, banner
import genice2.formats


class Format(genice2.formats.Format):
    """
Output the atomic positions in Yaplot format.

Options:
    H=x   Set the radius of H to be x
    """
    size_H = 0.01


    def __init__(self, **kwargs):
        unknown = dict()
        for k, v in kwargs.items():
            if k == "H":
                self.size_H = float(v)
            else:
                unknown[k] = v
        super().__init__(**unknown)


    def hooks(self):
        return {1:self.Hook1,
                2:self.Hook2,
                6:self.Hook6,
                7:self.Hook7}


    @timeit
    @banner
    def Hook1(self, ice):
        "Draw the cell in Yaplot format."
        logger = getLogger()
        s = yp.Layer(2)
        x,y,z = ice.repcell.mat
        for p,q,r in ((x,y,z),(y,z,x),(z,x,y)):
            for a in (np.zeros(3), p, q, p+q):
                s += yp.Line(a,a+r)
        self.output = s


    @timeit
    @banner
    def Hook2(self, ice):
        "Output CoM of water molecules in Yaplot format."
        logger = getLogger()
        if self.size_H > 0:
            return
        # prepare the reverse dict
        waters = defaultdict(dict)
        pos = ice.reppositions @ ice.repcell.mat
        s = ""
        for p in pos:
            s += yp.Layer(4)
            s += yp.Color(3)
            s += yp.Size(0.03)
            s += yp.Circle(p)
        self.output += s + yp.NewPage()
        return True


    @timeit
    @banner
    def Hook6(self, ice):
        "Output water molecules in Yaplot format."
        logger = getLogger()
        logger.info("  Total number of atoms: {0}".format(len(ice.atoms)))
        # prepare the reverse dict
        waters = defaultdict(dict)
        for atom in ice.atoms:
            resno, resname, atomname, position, order = atom
            if "O" in atomname:
                waters[order]["O"] = position
            elif "H" in atomname:
                if "H0" not in waters[order]:
                    waters[order]["H0"] = position
                else:
                    waters[order]["H1"] = position
        s = ""
        s += yp.Color(3)
        for order, water in waters.items():
            O = water["O"]
            H0 = water["H0"]
            H1 = water["H1"]
            s += yp.Layer(4)
            s += yp.Color(3)
            s += yp.Size(0.03)
            s += yp.Circle(O)
            s += yp.Line(O,H0)
            s += yp.Line(O,H1)
            s += yp.Size(self.size_H)
            s += yp.Circle(H0)
            s += yp.Circle(H1)
            s += yp.Color(2)
            s += yp.Layer(1)
            s += yp.Text(O, "{0}".format(order))
        s += yp.Layer(3)
        s += yp.Color(4)
        s += yp.ArrowType(1)
        s += yp.Size(0.03)
        for i,j in ice.spacegraph.edges(data=False):
            if i in waters and j in waters:  # edge may connect to the dopant
                O = waters[j]["O"]
                H0 = waters[i]["H0"]
                H1 = waters[i]["H1"]
                d0 = H0 - O
                d1 = H1 - O
                rr0 = np.dot(d0,d0)
                rr1 = np.dot(d1,d1)
                if rr0 < rr1 and rr0 < 0.245**2:
                    s += yp.Arrow(H0,O)
                if rr1 < rr0 and rr1 < 0.245**2:
                    s += yp.Arrow(H1,O)
        self.output += s
        self.nwateratoms = len(ice.atoms)


    @timeit
    @banner
    def Hook7(self, ice):
        "Output water molecules in Yaplot format."
        logger = getLogger()
        logger.info("  Total number of atoms: {0}".format(len(ice.atoms)))
        gatoms = ice.atoms[self.nwateratoms:]
        palettes = dict()
        s = ""
        s += yp.Layer(4)
        s += yp.ArrowType(1)
        H = []
        O  = ""
        for atom in gatoms:
            resno, resname, atomname, position, order = atom
            if atomname in palettes:
                pal = palettes[atomname]
            else:
                pal = 4 + len(palettes)
                palettes[atomname] = pal
            s += yp.Color(pal)
            s += yp.Size(0.04)
            s += yp.Circle(position)
        s = '#' + "\n#".join(ice.doc) + "\n" + s
        s += yp.NewPage()
        self.output += s

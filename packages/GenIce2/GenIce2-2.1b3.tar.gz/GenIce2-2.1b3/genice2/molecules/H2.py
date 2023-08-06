# coding: utf-8

desc={"ref": {"H2": "https://www.britannica.com/science/hydrogen"},
      "brief": "Hydrogen molecule.",
      "usage": "No options available."
      }

import numpy as np
from logging import getLogger
import genice2.molecules

class Molecule(genice2.molecules.Molecule):
    def __init__(self):
        self.sites_ = np.array([[0,0,-0.037],
                               [0,0,+0.037]])   # nm, HH

        self.labels_ = ["H","H"]
        self.name_ = "H2"

# coding: utf-8
import numpy as np

from logging import getLogger
import genice2.molecules.one


desc={
      "usage": "No options available.",
      "brief": "A united-atom methane model."
      }


class Molecule(genice2.molecules.one.Molecule):
    def __init__(self):
        super().__init__(label="Me", name="Me")

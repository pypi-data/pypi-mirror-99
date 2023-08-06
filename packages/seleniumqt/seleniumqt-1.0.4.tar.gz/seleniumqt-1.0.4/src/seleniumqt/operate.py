#coding: utf-8
import os
from seleniumqt.f2def import funct
from seleniumqt import highLightElement


def run(p):
    highLightElement.run(p[0], p[1], 2)
    return funct(os.path.basename(__file__), p)

#coding: utf-8
import os
from seleniumqt.f2def import funct


def run(p):
    t = funct(os.path.basename(__file__), p)
    return t

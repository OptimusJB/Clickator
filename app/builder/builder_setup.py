from setuptools import setup
from Cython.Build import cythonize

fichier = open("pybuild.txt", "r")
fichier_read = fichier.read()
fichier.close()
setup(ext_modules=cythonize(fichier_read))
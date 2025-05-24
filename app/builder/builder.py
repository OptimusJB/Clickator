"""
ce fichier fonctionne avec builder_setup.py
compile tous les fichiers python dans le même dossier grâce à cython, puis lance main
"""
import os

def create_app():
    if "pybuild" in os.listdir():
        fichier = open("pybuild.txt", "r")
        fichier_read = fichier.read()
        fichier.close()

        if fichier_read == "done":
            return None

    liste_py = []
    for element in os.listdir():
        if element[len(element) - 3:] == ".py":
            liste_py.append(element)

    for element in liste_py:
        fichier = open("pybuild.txt", "w")
        fichier.write(element)
        fichier.close()
        os.system("python builder_setup.py build_ext --inplace")

    os.mkdir("fichiers python")
    for element in liste_py:
        fichier = open(element, "rb")
        fichier_read = fichier.read()
        fichier.close()

        fichier = open("fichiers python/" + element, "wb")
        fichier.write(fichier_read)
        fichier.close()

    for element in liste_py:
        if not element == "builder.py":
            os.remove(element)

    fichier = open("pybuild.txt", "w")
    fichier.write("done")
    fichier.close()

create_app()
import main
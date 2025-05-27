import os
class Settings:
    """
    si le fichier settings.txt est changé, les changements seront effectifs au prochain lancement de Clickator
    """
    def __init__(self):
        if not "settings.txt" in os.listdir():
            fichier = open("settings.txt", "w")

            # le """ doit être sur la même ligne que le premier setting
            fichier.write("""degré de ressemblance image=0.9
temps entre les actions (em ms)=100
touche d'arrêt de la macro=p
bouton changement coordonnées=p""") # le """ doit être sur la même ligne que le dernier setting
            fichier.close()

        # chargement du fichier settings.txt
        fichier = open("settings.txt", "r")
        fichier_read = fichier.read()
        fichier.close()

        # création du dico valeurs
        self.settings = {}  # clé et valeurs sous forme de str
        for element in fichier_read.split("\n"):
            self.settings[element.split("=")[0]] = element.split("=")[1]

        assert len(self.settings.keys()) == len(fichier_read.split("\n")), "il semble y avoir deux settings avec le même nom"

    def get_value(self, valeur):
        assert valeur in self.settings.keys(), "la valeur " + str(valeur) + " n'existe pas"
        return self.settings[valeur]

settings = Settings()   # à utiliser directement dans le code
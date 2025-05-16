class Save:
    def __init__(self):
        self.contenu = None
    
    def load_sauvegarde(chemin_fichier):
        fichier = open("save.txt", "r")
        fichier_read = fichier.read()
        fichier.close()

save = Save()
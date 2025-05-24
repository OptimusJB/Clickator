from Chiffrement import chiffreur
from Clic import Clic

class Save:
    def __init__(self):
        self.contenu = None
        self.conversion = {"Clic":Clic}    # dictionnaire : clé = nom, valeur = objet correspondant au nom : utilisé pour load_sauvegarde
    
    def load_sauvegarde(self, nom_fichier):   # nom fichier sans extension
        fichier = open("data/" + nom_fichier + ".txt", "r")
        fichier_read = fichier.read()
        fichier.close()

        self.contenu = [nom_fichier]
        fichier_read = chiffreur.dechiffrer(fichier_read)
        for element in fichier_read.split("&slelement&"):
            truc = element.split("&slvaleur&")
            if not truc == [""]:
                self.contenu.append(truc)
        
        # chargement
        liste = [self.contenu[0]]
        for element in self.contenu[1:]:
            liste.append(self.conversion[element[0]](element[1:]))
        
        self.contenu = liste
        return self.contenu
    
    def sauvegarder(self, contenu:list):
        """
        liste de la forme [nom macro, element, element, element]
        """
        chaine = ""
        for element in contenu[1:]:
            valeurs = ""
            for valeur in element.valeurs:
                valeurs = valeurs + str(valeur) + "&slvaleur&"
            
            valeurs = valeurs[:len(valeurs) - len("&slvaleur&")]
            chaine = chaine + element.nom + "&slvaleur&" + valeurs + "&slelement&"
        chaine = chaine[:len(chaine) - len("&slelement&")]

        fichier = open("data/" + contenu[0] + ".txt", "w") # contenu[0] est le nom sans extension
        fichier.write(chiffreur.chiffrer(chaine))
        fichier.close()

save = Save()
save.sauvegarder(["test sauvegarde", Clic([1, 2, 3, 4, 5])])
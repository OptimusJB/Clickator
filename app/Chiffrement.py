import random

class Chiffrement:
    def __init__(self, liste_data:list):
        liste_data = list(liste_data)   # pour éviter un effet de bord
        assert type(liste_data) == list, "liste_data doit être une liste"
        assert len(liste_data) <= 10**2, "liste_data est trop grand"
        self.database = []

        liste = []
        taille = 0
        while len(liste_data) != 0:
            taille = taille + 1
            assert len(liste_data[0]) == 1, "les caractères à chiffrer doivent être un seul caractère"
            liste.append(liste_data[0])
            liste_data.pop(0)

            if taille == 10:
                self.database.append(liste)
                liste = []
                taille = 0
        
        if len(liste) != 0:
            self.database.append(liste)
    
    def find_numero(self, lettre):
        index_ligne = -1
        for ligne in self.database:
            index_ligne = index_ligne + 1
            if lettre in ligne:
                return str(index_ligne) + str(ligne.index(lettre))
        raise ValueError("la lettre " + lettre + " n'est pas disponible")

    
    def chiffrer(self, texte:str):
        assert type(texte) == str, "texte doit être une chaine de caractères"
        texte_final = ""
        for lettre in texte:
            texte_final = texte_final + self.find_numero(lettre)
        multiple = random.randint(1, 9)

        if texte_final == "":
            return ""
        return str(multiple) + str(int(texte_final) * multiple)
    
    def dechiffrer(self, texte_numero:str):
        assert type(texte_numero) == str, "texte_numero doit être un texte"
        if texte_numero == "":
            return ""
        texte_numero = str(int(texte_numero[1:]) // int(texte_numero[0]))

        # split du texte
        liste_valeurs = []
        avancement = 0
        texte_min = ""
        while avancement < len(texte_numero):
            texte_min = texte_min + texte_numero[avancement]
            if avancement % 2 == 1:
                liste_valeurs.append(texte_min)
                texte_min = ""
            avancement = avancement + 1

        texte_final = ""
        for numero in liste_valeurs:
            texte_final = texte_final + self.database[int(numero[0])][int(numero[1])]
        return texte_final

lettres = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
lettres_maj = []
for lettre in lettres:
    lettres_maj.append(lettre.upper())
chiffres = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
autres = [",", ";", "/", "#", "@", "é", "à", "ç", "(", ")", "&", " ", ".", "/"]   # pas de "-" pour éviter les nombres négatifs

all_lettres = lettres + lettres_maj + chiffres + autres

chiffreur = Chiffrement(all_lettres)
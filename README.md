# Clickator

## Présentation
Clickator est un logiciel permettant de créer et gérer des macros

## Comment utiliser
tout d'abord, pour créer une macro, il faut entrer un nom de macro en bas à gauche, puis cliquer sur "créer macro". Ensuite, il devient possible d'ajouter des actions. En cliquant sur l'action ajoutée, il est possible de changer certains paramètres (les coordonnées du TP par exemple). Enfin, il suffit juste de cliquer sur "lancer macro" ou appuyer sur p (par défaut) pour lancer la macro sélectionnée.  
Il est possible de changer divers paramètres dans le fichier settings.txt

## Liste des actions
- Clic : permet de faire un clic
- Wait : permet de mettre en pause la macro pendant un certain laps de temps, ou jusqu'à ce que une ou plusieurs touches soit pressées
- TP : permet de téléporter le curseur sur des coordonnées ou une image présente sur l'écran
- Mouvement : permet de bouger le curseur vers des coordonnées ou une image présente sur l'écran
- Touche : permet de presser une touche du clavier
- Scroll : permet de scroller ('longueur' signifie le nombre de scroll)
- ReturnStart : permet de revenir au début de la macro (boucle)

## Quelques détails
- TP et Mouvement : possibilité de changer x et y avec la touche c (par défaut)
- TP et Mouvement : si l'image n'est pas trouvée sur l'écran, le curseur ne bougera pas
- pour wait et touche : tous les caractères entrés seront pris en compte (wait va attendre que toutes les touches soient pressées, et touche va presser sur toutes les touches
- dans l'action Touche, mettre un ./ permet de considérer un mot, et non une lettre (ex : ./ctrl+shift+m)
- il est possible de mettre plusieurs lettres dans les settings
- la dispersion n'ajoute qu'en positif (le temps / coordonnées de base sont le minimum)
- le logiciel recrée settings.txt avec les paramètres de base s'il n'est pas là
- en faisant shift + clic sur une action, l'action est clonée

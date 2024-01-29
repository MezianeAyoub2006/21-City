Merci d'essayer Pokemon-SLASH.

Pour jouer demmarez main.py ou le fichier main.exe.

<modules utilisés>

* pygame-ce 2.4.0, pygame peut suffire
* pyperclip
* numpy
* pillow

Voilà quelques directives qui vous aiderons lors de vos parties : 

<touches>

ENTER / ENTREE : Valider le fait de jouer dans le menu
SPACE / ESPACE : Utiliser un objet ou attaquer avec
e / E : Traverser le portail à la fin de chaque niveau
F11 : Mettre en plein écran
P : Mettre en pause
RETURN / SUPPR : Jeter un objet de l'inventaire

<conseils généraux>

* Essayez de tuer un maximum de pokémons avant chaque boss, cela vous permettra 
d'avoir plus de niveaux et de potions.

* Prenez le moins de dégats avant chaque boss, gardez à l'esprit que votre vie est 
restaurée à la complétion de chaque niveau.

* Affrontez en priorité les pokemons avec un niveau similaire au votre.

* Apprenez à éviter les attaques physiques en coutournant les ennemis après chaque
attaque.

* Gardez le plus souvent un espace de libre dans votre inventaire en jetant l'arme
que vous n'utilisez plus afin de pouvoir recueillir d'eventuels objets.

<conseils spécifiques>

* Pour les second et troisième boss, essayez de les contourner de de les enchainer 
d'attaques quand ils vous suivent.

* Pour le quatrième boss, apprenez à contourner ses attaques et à rester à distance
de lui.

<commandes>

Ce n'est pas précisé dans le cahiet des charges puisque ce n'est pas un ajout "officiel"
mais propre aux développeurs, il est possible d'utiliser des commandes dans le jeu afin
d'effectuer divers tests et ajustements.

Pour pouvoir utiliser les commandes voilà la marche à suivre : 

* En jeu, appuyer sur P puis rien d'autre.
* Tappez ensuite DEBUG_MODE "dans le vide" 
* Pressez la touche ENTER / ENTREE

Vous verrez un champ de texte apparaitre et vous pourrez tapper
des commandes dans celui-ci. Il est également possible de coller 
une commande stockée dans le presse papier avec CTRL + V.

Voilà la liste des commandes : 

* /default : remet les changements opérés par commandes à des valeurs par défaut
* /heal : soigne le joueur
* /clip : permet au joueur de traverser ou non les murs
* /kill : tue le joueur
* /debug : permet de voir ou non les éléments de débogage

* /portal niveau : fait apparaitre un portail qui redirige vers "niveau"
* /speed speed : met la vitesse du joueur à "speed"
* /life life : met la vie du joueur à "life"
* /level level : met le niveau du joueur à "level"
* /tick tick : accélère le jeu de "tick"
* /inventory inventory : change l'inventaire du joueur à "inventory"

* /tp x y : téléporte le joueur à la position ("x", "y")
* /give item number : donne l'objet "item" au nombre de "number" au joueur
* /define variable value : crée une variable "variable" avec la valeur "value" en elle

* /spawn id level x y : fait apparaitre un pokémon d'id "id" de niveau "level" à la position ("x", "y")
* /loop idx begin end step : boucle la prochaine instruction avec l'index "idx", débutant par "begin", se terminant par "end", avec un pas "step"

Voilà quelques commandes intéréssantes à tester pour vous, copier collez les une par une :

[APPARITION DE 100 POKEMONS]
/loop i 0 100 1 
/spawn randint(0,60) randint(1,100) randint(2,23) randint(2,23)

[JEU RALENTI, JOUEUR RAPIDE]
/tick 0.3
/speed 10

[JOUEUR SUR-PUISSANT]
/level 100
/inventory [[2, 1], [3, 1], [7, 10]]

[CONFIGURATION DEBOGAGE]
/level 100
/speed 5
/debug
/clip
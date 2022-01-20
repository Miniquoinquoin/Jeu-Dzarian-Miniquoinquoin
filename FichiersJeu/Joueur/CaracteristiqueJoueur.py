"""Fichier Contenant la Base des fonctionaliter du Joueur"""


import FichiersJeu.Interface.EZ as EZ

class Joueur:
    """Class joueur"""

    def __init__(self, name, level, personnage = "Perso1", stats = {"vie": 100, "damage": 10, "speed": 5 }, equipement = None):
        """Initialisation de Joueur

        Args:
            name (str): nom du joueur
            level (int): level du joueur
            personnage(str): nom du personnage
            stats (dic): toutes les stats du joueur [heal,dammage,speed]
            equipement (dic): Toutes ces objet [weapon, shield]
        """
        self.name = name
        self.level = level
        self.personnage = personnage
        self.stats = stats
        self.equipement = equipement
        self.x = 1240//2
        self.y = 470  #Hauteur de base du joueur
        self.move_info = {"right": False, "left": False}

        self.charges = None  #Si l'image est chargé ou non

    def charge(self):
        """Foncton qui charge l'image du personage"""

        if self.personnage == "Perso1":
            self.chargesAvant = EZ.transforme_image(EZ.charge_image("..\Jeu-Dzarian-Miniquoinquoin\FichiersJeu\Interface\Entites\Items\Personnages\Perso1\Perso1A1.png"), 0, 3)
            self.chargesDroite = EZ.transforme_image(EZ.charge_image("..\Jeu-Dzarian-Miniquoinquoin\FichiersJeu\Interface\Entites\Items\Personnages\Perso1\Perso1A7.png"), 0, 3)
            self.chargesGauche = EZ.transforme_image(EZ.charge_image("..\Jeu-Dzarian-Miniquoinquoin\FichiersJeu\Interface\Entites\Items\Personnages\Perso1\Perso1A4.png"), 0, 3)


    def display(self):
        """Fonction qui trace le Joueur

        Args:
            x (int): x du joueur
            y (int): y du joueur
        """

        if self.charges == None:
            self.charge()
        
        self.move()

        EZ.trace_image(self.charges, self.x, self.y)

    """
    def moveRight(self):
        Deplace le joueur vers la droite
        self.x += self.stats["speed"]

    
    def moveLeft(self):
        Deplace le joueur vers la Gauche
        self.x -= self.stats["speed"]
    """

    def move(self):

        if self.move_info["right"] == True:
            #self.moveRight()
            self.charges = self.chargesDroite

        
        elif self.move_info["left"] == True:
            #self.moveLeft()
            self.charges = self.chargesGauche
        
        else:
            self.charges = self.chargesAvant
        

        
        

    


        



    







    




"""Fichier contenant l'ensemble des menu du jeu"""

import FichiersJeu.Interface.EZ as EZ
import FichiersJeu.Joueur.CaracteristiqueJoueur as CJ
import FichiersJeu.Interface.Entites.Bouton as Bouton



class Interface:
    """Class mere de toute les interface"""

    def __init__(self, longeur, hauteur):
        self.longeur = longeur
        self.hauteur = hauteur
        


class Menu(Interface):
    """Class du menu de base"""

    def __init__(self, longeur, hauteur):
        super().__init__(longeur, hauteur)

        self.chargesFond = None
        self.decal = 0
        self.longeur = longeur
        self.hauteur = hauteur


    
    def chargeFond(self):
        """Charge l'image du fond"""

        self.chargesFond = EZ.charge_image("..\Jeu-Dzarian-Miniquoinquoin\FichiersJeu\Interface\Entites\Fond\Fond_menu2.png")

    def displayFond(self):
        """Trace le fond du menu"""

        if self.chargesFond == None:
            self.chargeFond()

        EZ.trace_image(self.chargesFond ,0,0)
    
    def displayPlayer(self,image):
        """Trace le personnage"""

        EZ.trace_image(EZ.transforme_image(image,0,2), self.longeur//2-144, self.hauteur//2-144) # -144 pour le centrer, je sais pas pourquoi
    
    def displayBoutonPlay(self):

        Bouton.BoutonPlayMenu(465, 550)

    
    def displayMenu(self, personnage):
        """Trace le Menu"""

        self.displayFond()
        self.displayPlayer(personnage)
        self.displayBoutonPlay()


class Game(Interface):

    def __init__(self, longeur, hauteur):
        super().__init__(longeur, hauteur)

        self.chargesFond = None
        self.decal = 1200

        self.move_info = {"right": False, "left": False, "saut": False, "rightSaut": False, "leftSaut": False}


    def chargeFond(self):
        """Charge l'image du fond"""

        self.chargesFond = EZ.charge_image("..\Jeu-Dzarian-Miniquoinquoin\FichiersJeu\Interface\Entites\Fond\FondGame.jpg")
    
    def displayFond(self, vitesse):
        """Trace le fond du jeu"""

        if self.chargesFond == None:
            self.chargeFond()
        
        self.move(vitesse)

        while not(0 <= self.decal <= 1200):
            if self.decal > 1200:
                self.decal -= 1200

            elif self.decal < 0:
                self.decal += 1200
        

        decal_x = [self.decal - 1200, self.decal] #Petit pertit bug sur la droite avec une certaine config 3 image = plus de lag

        for fond in range(2):
            EZ.trace_image(self.chargesFond ,decal_x[fond],-100)

        
    

    def move(self, vitesse):

        if not(self.move_info["saut"]):
            self.move_info["rightSaut"] = self.move_info["right"]
            self.move_info["leftSaut"] = self.move_info["left"]


            if self.move_info["right"] == True:
                self.decal -= vitesse

            
            elif self.move_info["left"] == True:
                self.decal += vitesse


        else:
            if self.move_info["rightSaut"] == True:
                self.decal -= vitesse

            
            elif self.move_info["leftSaut"] == True:
                self.decal += vitesse


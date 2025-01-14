"""Fichier contenant l'ensemble des menu du jeu"""

from ctypes import sizeof
from operator import eq
import FichiersJeu.Interface.EZ as EZ
import FichiersJeu.Joueur.CaracteristiqueJoueur as CJ
import FichiersJeu.Interface.Animation as Anim

import FichiersJeu.Interface.Decor as Decor
import FichiersJeu.Interface.Entites.Bouton as Btn

import FichiersJeu.InfoJoueur.ReadInfo as Reader

import Outiles.PerfCompteur as Perfcompteur
Perfcompt = Perfcompteur.TimeDistribution()



class Interface:
    """parent class for all the interface
    Class mere de toute les interface"""

    def __init__(self, longeur, hauteur):
        self.longeur = longeur
        self.hauteur = hauteur
        


class Menu(Interface):
    """Basic class for all the menu
    Class du menu de base"""

    def __init__(self, longeur, hauteur):
        super().__init__(longeur, hauteur)

        self.chargesFond = None
        self.longeur = longeur
        self.hauteur = hauteur


    def displayFond(self):
        """Display the background
        Trace le fond du menu"""

        if self.chargesFond == None:
            self.chargeFond()

        EZ.trace_image(self.chargesFond ,0,0)
    

    def displayPlayer(self,image):
        """Trace le personnage"""

        EZ.trace_image(EZ.transforme_image(image,0,2), self.longeur//2-144, self.hauteur//2-144) # -144 pour le centrer, 48*6 / 2


class MenuPricipale(Menu):
    """class of the main menu
    Classe du menu principal"""

    def __init__(self, longeur, hauteur):
        super().__init__(longeur, hauteur)
        self.etapeAnimationFond = 0 # etape de l'animation du fond
        
    def chargeFond(self):
        """ load the background image
        Charge l'image du fond"""

        self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\Fond_menu2.png")

    def displayAnimationFond(self):
        """Trace l'animation de fond du menu"""
        Anim.traceAnimationFondMenuP(self.longeur, self.hauteur, self.etapeAnimationFond)
        if self.etapeAnimationFond < self.hauteur * 2:
            self.etapeAnimationFond += 1
        
        else:
            self.etapeAnimationFond = 0
    
    def displayMenu(self, personnage, gold):
        """ draw the menu
        Trace le Menu"""

        self.displayAnimationFond()
        self.displayFond() # Les boutton de l'interface
        self.displayPlayer(personnage)
        Decor.nombreDeGold(900, 10, gold)

class MenuDeath(Menu):
    """player death menu"
    Menu de mort du joueur"""

    def __init__(self, longeur, hauteur):
        super().__init__(longeur, hauteur)

    def chargeFond(self):
        """ load the background image
        Charge l'image du fond"""

        self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMort.png")

    def displayFond(self, longeur, hauteur, gold, kill, wave, player,win):
        """Drawn the animation of Death Menu
        Trace l'animation du menu de la mort du joueur
        """
        Anim.traceAnimationMenuMort(longeur, hauteur, 3, gold, kill, wave, player, win)


class MenuGame(Menu):

    def __init__(self, longeur, hauteur):
        super().__init__(longeur, hauteur)

    def chargeFond(self):
        """ load the background image
        Charge l'image du fond"""

        self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\MenuGame.png")


class SousMenu(Menu):
    """class for all the submenu
    Classe pour tout les sous menu"""

    def __init__(self, longeur, hauteur, texte):
        super().__init__(longeur, hauteur)
        self.tailleOmbrePolice = 3 # Size of the Shadow of the fonts / Taille de l'ombre de la police
        self.yDebutWidget = self.hauteur//6 # y Start of the widget / y de début du Widget
        self.hauteurWidget = int(3 * self.hauteur/4) # height of the widget / Hauteur du widget
        self.couleurBorder = (100, 100, 110) # color of the border / couleur de la bordure
        self.couleurFond = (210, 210, 230) # color of the background / couleur du fond

        #Police
        self.texte = texte
        self.police = EZ.charge_police(50, "FichiersJeu\Interface\Entites\Police\CourageRoad.ttf", True)
        self.coordonneesFonts = [self.longeur//2 - EZ.dimension(EZ.image_texte(texte, self.police, 0, 0, 0))[0], self.yDebutWidget- EZ.dimension(EZ.image_texte(texte, self.police, 0, 0, 0))[1]] # [x, y]
        
        self.chargesPersonnage = {} # Dictonary of the player's image / Dictionnaire des images du joueur



    def chargeFond(self):
        """ load the background image
        charge l'image du fond"""

        self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondSousMenu.png")


    def traceTitre(self):
        """Draw the title of the subMenu
        trace le titre du sous-Menu

        Args:
            texte (str): Texte to drawn / texte a afficher
        """


        EZ.trace_image(EZ.image_texte(self.texte, self.police, 0, 0, 0), self.coordonneesFonts[0] + self.tailleOmbrePolice , self.coordonneesFonts[1] + self.tailleOmbrePolice)
        EZ.trace_image(EZ.image_texte(self.texte, self.police, 255, 255, 255), self.coordonneesFonts[0], self.coordonneesFonts[1])

    def traceFlecheRetour(self):
        """Draw the back arrow
        Trace la flèche retour
        """

        Decor.traceFlecheRetour(20, 20, 0.5)


    def TraceWidget(self, longueur):
        """Drawn the widget of the subMenu
        trace le widget(interface centré) du sous-Menu

        longueur (int): lenght of the widget / longueur du widget
        """
        
        Decor.traceCadre(self.longeur//2 - longueur//2, self.yDebutWidget, longueur, self.hauteurWidget, 3, 2, self.couleurFond, self.couleurBorder)
        
        self.traceTitre()
        self.traceFlecheRetour()

    def chargePersonnage(self):
        """load Caracters
        Charges les personnages
        """

        self.chargesPersonnage = {"Personnage1": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso1\Perso1A2.png"), 0, 5),
        "Personnage2": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso2\Perso2A2.png"), 0, 5), 
        "Personnage3": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso3\Perso3A2.png"), 0, 5), 
        "Personnage4": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso4\Perso4A2.png"), 0, 5), 
        "Personnage5": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso5\Perso5A2.png"), 0, 5),
        "Personnage6": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso6\Perso6A2.png"), 0, 5),
        "Personnage7": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso7\Perso7A2.png"), 0, 5), 
        "Personnage8": EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\Personnages\Perso8\Perso8A2.png"), 0, 5) }


class SlideMenu(SousMenu):
    """Class for the slide menu
    Classe pour le slide menu"""

    def __init__(self, longeur, hauteur, texte):
        super().__init__(longeur, hauteur, texte)
        self.hauteurCadre = int(3 * self.hauteurWidget/4)
        self.hauteurCardreInfo = int(3 * self.hauteurWidget/5)
        self.largeurCadre = 300
        self.largeurCadrePlusEspace = self.largeurCadre//0.9 # largeur du cadare plus l'espace qu'il laisse après lui pour ne pas être coller au prochain
        self.yDebutCadre = (self.hauteurWidget - self.hauteurCadre)//2 + self.yDebutWidget # y de début du cadre

        self.couleurFondCadre = (180, 180, 180) # couleur de fond des cadres
        self.couleurBordureCadre = (140, 140, 140) # couleur de la bordure des cadres
        self.policeCadre = EZ.charge_police(50, "FichiersJeu\Interface\Entites\Police\PermanentMarker-Regular.ttf", True)


      

    def TraceWidget(self, x, listeImages):
        """Drawn the widget of the slide Menu
        trace le widget du Menu Slide

        x (int): offset of the Caracters frame / decalage des Cadre des personnages
        listeImages (list): list of the images to drawn / liste des images a afficher
        """

        if len(listeImages) * self.largeurCadrePlusEspace + 100 < self.longeur:
            Decor.traceCadre(x - 50, self.yDebutWidget, self.longeur - 100, self.hauteurWidget, 3, 2, self.couleurFond, self.couleurBorder)

        elif x + 150 >= 100:
            Decor.traceCadre(x - 50, self.yDebutWidget, self.longeur + 150, self.hauteurWidget, 3, 2, self.couleurFond, self.couleurBorder)
        
        elif x < -(len(listeImages) * self.largeurCadrePlusEspace - self.longeur):
            Decor.traceCadre(-10, self.yDebutWidget, 20 + (x + len(listeImages) * self.largeurCadrePlusEspace), self.hauteurWidget, 3, 2, self.couleurFond, self.couleurBorder)
        
        else:
            Decor.traceCadre(-10, self.yDebutWidget, self.longeur + 20, self.hauteurWidget, 3, 2, self.couleurFond, self.couleurBorder)
        
        self.traceTitre()
        self.traceFlecheRetour()
    
    def traceBasicCadre(self, x, texte):
        """Draw frames that move
        Trace les Cadre qui bougent

        x (int): offset of the Caracters frame / decalage des Cadre des personnages
        texte (str): text to drawn / texte a afficher
        """

        Decor.traceCadre(x, self.yDebutCadre, self.largeurCadre, 3 *self.hauteurCadre//4, 3, 2, self.couleurFondCadre, self.couleurBordureCadre) # Haut du cadre
        Decor.traceCadre(x, self.yDebutCadre + 3 *self.hauteurCadre//4, 300, self.hauteurCadre//4, 3, 2, self.couleurBordureCadre, self.couleurBordureCadre) # Bas du cadre

        EZ.trace_image(EZ.image_texte(texte, self.policeCadre, 255, 255, 255), x + self.largeurCadre//2 - EZ.dimension(EZ.image_texte(texte, self.policeCadre, 255, 255, 255))[0]//2, self.yDebutCadre + 7 * self.hauteurCadre//8 - EZ.dimension(EZ.image_texte(texte, self.police, 255, 255, 255))[1]//2) # Texte du cadre


class Menu2Choice(SousMenu):
    """Class to choice the game mode
    class pour choisir le mode de jeu"""

    def __init__(self, longeur, hauteur, texte):
        super().__init__(longeur, hauteur, texte)
        self.largeurWidget = self.longeur - 100
        self.couleurBorderCadre = (140, 140, 140) # external color of frames info / Couleur externe des cadre info
        self.couleurFondCadre = (180, 180, 180) # Background color of frames info / Fond des cadre info

    def traceImage(self):
        """Draw the images of button mode
        Trace les images des boutons mode
        """

        Decor.traceCadre(self.largeurWidget//2 - EZ.dimension(self.chargesBouton[0])[0]//2 - 3 + 50, self.yDebutWidget + self.hauteurWidget//3 - EZ.dimension(self.chargesBouton[0])[1]//2 - 25, EZ.dimension(self.chargesBouton[0])[0] + 3, EZ.dimension(self.chargesBouton[0])[1], 3, 2, self.couleurFondCadre, self.couleurBorderCadre) # Background / Fond
        EZ.trace_image(self.chargesBouton[0], self.largeurWidget//2 - EZ.dimension(self.chargesBouton[0])[0]//2 + 50, self.yDebutWidget +  1 * self.hauteurWidget//3 - EZ.dimension(self.chargesBouton[0])[1]//2 - 25)

        Decor.traceCadre(self.largeurWidget//2 - EZ.dimension(self.chargesBouton[1])[0]//2 - 3 + 50, self.yDebutWidget + 2 * self.hauteurWidget//3 - EZ.dimension(self.chargesBouton[1])[1]//2 + 25, EZ.dimension(self.chargesBouton[1])[0] + 3, EZ.dimension(self.chargesBouton[1])[1], 3, 2, self.couleurFondCadre, self.couleurBorderCadre) # Background / Fond
        EZ.trace_image(self.chargesBouton[1], self.largeurWidget//2 - EZ.dimension(self.chargesBouton[1])[0]//2 + 50, self.yDebutWidget + 2 * self.hauteurWidget//3 - EZ.dimension(self.chargesBouton[0])[1]//2 + 25)
    
    def DisplayMenu(self):
        """Display all the Menu
        Trace tout le Menu
        """

        self.displayFond()
        self.TraceWidget(self.largeurWidget)
        self.traceImage()

class Personnages(SlideMenu):
    """Player Menu class 
    Class du Menu des personnages"""

    def __init__(self, longeur, hauteur, texte, Inventaire = {}):
        super().__init__(longeur, hauteur, texte)
        self.hauteurCardreJoueur = int(3 * self.hauteurWidget/4)
        

        self.couleurFondCadreAchete = (200, 50, 50) 
        self.couleurBordureCadreAchete = (150, 0, 0) 

        self.couleurFondCadreEquipe = (50, 200, 50) 
        self.couleurBordureCadreEquipe = (0, 150, 0)


        self.policeCadre = EZ.charge_police(60, "FichiersJeu\Interface\Entites\Police\PermanentMarker-Regular.ttf", True)

    def chargePersonnage(self):
        super().chargePersonnage()

        self.largeurAllCadre = self.largeurCadrePlusEspace * len(self.chargesPersonnage)

    
    def TrieInventaire(self, Inventaire):
        """sort iventory to return Caracters infomartion
        Trie Inventaire et renvoie les inforamtion sur les personnages

        Args:
            Inventaire (dict): dictionary of inventoty / dictionnaire de l'inventaire
        """

        Personnages = {}
        for keys in Inventaire:
            if "Personnage" in keys:
                Personnages.update({keys: Inventaire[keys]})
        
        self.infoPersonnages = Personnages



    def traceCadreJoueur(self, x, etat):
        """Draw the frame for Caracters
        Trace le Cadre des Personnages

        Args:
            x (int): x start of frame / x début du Cadre
            etat (str): False: Caracters can by buy / Le personnages peut être acheter
                        True: Caracters can by play / Le personnages peut être jouer 
        """

        if etat:
            Decor.traceCadre(x, self.yDebutCadre, self.largeurCadre, 3 *self.hauteurCardreJoueur//4, 3, 2, self.couleurFondCadreEquipe, self.couleurBordureCadreEquipe) # Haut du cadre
            Decor.traceCadre(x, self.yDebutCadre + 3 *self.hauteurCardreJoueur//4, 300, self.hauteurCardreJoueur//4, 3, 2, self.couleurBordureCadreEquipe, self.couleurBordureCadreEquipe) # Haut du cadre

            coordonneesFonts = [x + self.largeurCadre//2 - EZ.dimension(EZ.image_texte("Select", self.policeCadre, 0, 0, 0))[0]//2, self.yDebutCadre + 7 *self.hauteurCardreJoueur//8 - EZ.dimension(EZ.image_texte("Select", self.policeCadre, 0, 0, 0))[1]//2] # [x, y]
            EZ.trace_image(EZ.image_texte("Select", self.policeCadre, 0, 0, 0), coordonneesFonts[0] + self.tailleOmbrePolice , coordonneesFonts[1] + self.tailleOmbrePolice)
            EZ.trace_image(EZ.image_texte("Select", self.policeCadre, 255, 255, 255), coordonneesFonts[0], coordonneesFonts[1])


        else:
            Decor.traceCadre(x, self.yDebutCadre, self.largeurCadre, 3* self.hauteurCardreJoueur//4, 3, 2, self.couleurFondCadreAchete, self.couleurBordureCadreAchete)
            Decor.traceCadre(x, self.yDebutCadre + 3 *self.hauteurCardreJoueur//4, 300, self.hauteurCardreJoueur//4, 3, 2, self.couleurBordureCadreAchete, self.couleurBordureCadreAchete) # Haut du cadre
            
            coordonneesFonts = [x + self.largeurCadre//2 - EZ.dimension(EZ.image_texte("Buy", self.policeCadre, 0, 0, 0))[0]//2,  self.yDebutCadre + 7 *self.hauteurCardreJoueur//8 - EZ.dimension(EZ.image_texte("Select", self.policeCadre, 0, 0, 0))[1]//2] # [x, y]
            EZ.trace_image(EZ.image_texte("Buy", self.policeCadre, 0, 0, 0), coordonneesFonts[0] + self.tailleOmbrePolice , coordonneesFonts[1] + self.tailleOmbrePolice)
            EZ.trace_image(EZ.image_texte("Buy", self.policeCadre, 255, 255, 255), coordonneesFonts[0], coordonneesFonts[1])



    def traceAllPersonnages(self, x):
        """Drawn all the Caracters and their frames
        Trace tout des personnages et leur cadre

        Args:
            x (int): x start of frames / x du debut des Cadres
        """

        if self.chargesPersonnage == {}:
            self.chargePersonnage()

        xStart = x
        for infoPersonnage, ImagePeronnage in zip(self.infoPersonnages,self.chargesPersonnage):
            self.traceCadreJoueur(xStart, self.infoPersonnages[infoPersonnage][0])
            EZ.trace_image(self.chargesPersonnage[ImagePeronnage], xStart + self.largeurCadre//2 - EZ.dimension(self.chargesPersonnage[ImagePeronnage])[0]//2, self.yDebutCadre + 20)
            xStart += self.largeurCadrePlusEspace
        
    
    def traceMenuPersonnages(self, x):
        """Drawn all the Menu of Caracters
        Trace tout le Menu des Personnages

        Args:
            x (int): x gap of widget / x du debut des Cadres
        """

        # Perfcompt.newElement("Fond")
        self.displayFond()
        # Perfcompt.EndElement()

        # Perfcompt.newElement("Widget")
        self.TraceWidget(x, self.chargesPersonnage)
        # Perfcompt.EndElement()


        # Perfcompt.newElement("Personnages")
        self.traceAllPersonnages(x)
        # Perfcompt.EndElement()

        # Perfcompt.calculate()
        # Perfcompt.clear()


class StatsPersonnage(SousMenu):
    """Class to display the Stats of a Caracter and is price
    Classe pour afficher les stats d'un personnage et son prix"""

    def __init__(self, longeur, hauteur, numPerso,texte, stats):
        super().__init__(longeur, hauteur, texte)
        self.stats = stats
        self.numPerso = numPerso

        self.largeurWidget = self.longeur - 100

        self.hauteurCardreInfo = int(3 * self.hauteurWidget/5)
        self.yDebutCadre = (self.hauteurWidget - self.hauteurCardreInfo)//4 + self.yDebutWidget
        self.largeurCadre = 400 # lenght of the Info Frame / longueur du cadre d'info

        self.chargeImageArme = EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme{self.numPerso + 1}\Arme{self.numPerso + 1}lvl1.png" ) # Load the image of the weapon / Charge l'image de l'arme
        self.tailleImage = [EZ.dimension(self.chargeImageArme)[0], EZ.dimension(self.chargeImageArme)[1]] # [largeur, hauteur]
        self.chargesImageArme = EZ.transforme_image(self.chargeImageArme, 0, 150/(self.tailleImage[1] if self.tailleImage[0] * 150/self.tailleImage[1] < self.largeurCadre else self.tailleImage[0]//2)) # give the perfect size at the picture / donne la taille idéale à l'image

        self.couleurBorderCadre = (140, 140, 140) # external color of frames info / Couleur externe des cadre info
        self.couleurFondCadre = (180, 180, 180) # Background color of frames info / Fond des cadre info

        self.policeCadre = EZ.charge_police(40, "FichiersJeu\Interface\Entites\Police\JosefinSans-BoldItalic.ttf", True)

    def traceCadre(self):
        """Drawn the frames for Caracters info
        Trace les Cadre pour les info du personnages
        """
        
        for Cadre in range(1, 3):
            xCadre = Cadre * self.largeurWidget//2.5 - 150
            Decor.traceCadre(xCadre, self.yDebutCadre, self.largeurCadre, self.hauteurCardreInfo, 2, 3, self.couleurFondCadre, self.couleurBorderCadre) # Background / Fond

    



    def traceJoueur(self):
        """Draw the player
        Trace le joueur
        """

        if self.chargesPersonnage == {}:
            self.chargePersonnage()

        EZ.trace_image(self.chargesPersonnage[f"Personnage{self.numPerso + 1}"], (self.largeurWidget//3) - 80 - EZ.dimension(self.chargesPersonnage[f"Personnage{self.numPerso + 1}"])[0], self.yDebutCadre + self.hauteurCardreInfo - EZ.dimension(self.chargesPersonnage[f"Personnage{self.numPerso + 1}"])[1])
        


        

    def DisplayMenu(self):
        """Display all the Menu
        Trace tout le Menu
        """

        self.displayFond()
        self.TraceWidget(self.largeurWidget)
        self.traceCadre()
        self.traceJoueur()


class BuyPersonnage(StatsPersonnage):
    """Class for the menu to buy a personnage
    Classe pour le menu d'achat d'un personnage"""

    def __init__(self, longeur, hauteur, numPerso, texte, stats):
        super().__init__(longeur, hauteur, numPerso, texte, stats)

    def traceCadreInfo(self):
        """Drawn the Caracters info
        Trace les info du personnages
        """
        
        for Cadre in range(1, 3):
            xCadre = Cadre * self.largeurWidget//2.5 - 150

            if Cadre == 1:
                # Picture of the weapon / Image de l'arme
                EZ.trace_image(self.chargesImageArme, xCadre + self.largeurCadre//2 - EZ.dimension(self.chargesImageArme)[0]//2, self.yDebutCadre + self.hauteurCardreInfo//4 - EZ.dimension(self.chargesImageArme)[1]//2)

                # Weapon Stats / Stats de l'arme
                EZ.trace_image(EZ.image_texte(f"Damage: {self.stats['weapon']['damage']}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 160)
                EZ.trace_image(EZ.image_texte(f"Range: {self.stats['weapon']['range']}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 110)
                EZ.trace_image(EZ.image_texte(f"Durability: {self.stats['weapon']['durability']}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 60)


            elif Cadre == 2:
                # Caracters stats / Stats du personnage
                EZ.trace_image(EZ.image_texte(f"Health: {self.stats['vie']}", self.policeCadre), xCadre + 10, self.yDebutCadre + 10)
                EZ.trace_image(EZ.image_texte(f"Regen Time: {self.stats['regen']['cooldown']}", self.policeCadre), xCadre + 10, self.yDebutCadre + 60)
                EZ.trace_image(EZ.image_texte(f"Regen Power: {float(self.stats['regen']['eficiency']) * 10} ", self.policeCadre), xCadre + 10, self.yDebutCadre + 110)
                EZ.trace_image(EZ.image_texte(f"Speed: {self.stats['speed']}", self.policeCadre), xCadre + 10, self.yDebutCadre + 160)
                EZ.trace_image(EZ.image_texte(f"Acc: {self.stats['acc']}", self.policeCadre), xCadre + 10, self.yDebutCadre + 210)
                EZ.trace_image(EZ.image_texte(f"Jump Power: {self.stats['jumpPower']}", self.policeCadre), xCadre + 10, self.yDebutCadre + 260)


    def tracePrix(self):
        """Draw the price of the Caracters
        Trace le prix du Personnage
        """
        Decor.nombreDeGold(self.longeur - self.largeurWidget, self.yDebutWidget + self.hauteurWidget - 100, self.stats['price'])
    
    def traceBouttonBuy(self):
        """Draw the buy button
        Trace le bouton play
        """

        Btn.Bouton(self.largeurWidget - 200, self.yDebutWidget + self.hauteurWidget - 100, 200, 80, "Buy", (255, 255, 255), (0, 128, 64), 1, 3)
    



    def DisplayMenu(self):
        super().DisplayMenu()
        self.traceCadreInfo()
        self.tracePrix()
        self.traceBouttonBuy()

class Mode(Menu2Choice):
    """Class to choice the game mode
    class pour choisir le mode de jeu"""

    def __init__(self, longeur, hauteur, texte):
        super().__init__(longeur, hauteur, texte)
        self.chargesBouton = [EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Mode\BoutonCampagne.png"), EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Mode\BoutonInfini.png")]


class Infini(SlideMenu):
    """Class to choice the map for mode Infini
    class pour choisir la carte pour le mode Infini"""

    def __init__(self, longeur, hauteur, texte):
        super().__init__(longeur, hauteur, texte)
        self.largeurWidget = self.longeur - 100

        self.chargesMap = { "Terre": EZ.selectionne_partie_image(EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Terre.jpg"), 0, 400, self.largeurCadre - 50, self.hauteurCardreInfo - 50), 
        "Mars": EZ.selectionne_partie_image(EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Mars.png"), 0, 400, self.largeurCadre - 50, self.hauteurCardreInfo - 50),
        "Gluton": EZ.selectionne_partie_image(EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Gluton.jpg"), 50, 400, self.largeurCadre - 50, self.hauteurCardreInfo - 50),
        "Volcano": EZ.selectionne_partie_image(EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Volcano.jpg"), 0, 400, self.largeurCadre - 50, self.hauteurCardreInfo - 50),
        "Forestia": EZ.selectionne_partie_image(EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Forestia.jpg"), 0, 400, self.largeurCadre - 50, self.hauteurCardreInfo - 50),
        "Dead Zone": EZ.selectionne_partie_image(EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\DeadZone.jpg"), 0, 400, self.largeurCadre - 50, self.hauteurCardreInfo - 50),
        "Candya": EZ.selectionne_partie_image(EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Candya.jpg"), 0, 400, self.largeurCadre - 50, self.hauteurCardreInfo - 50),
        }

        self.largeurAllCadre = self.largeurCadrePlusEspace * len(self.chargesMap)

    def traceAllCadre(self,x):
        """Draw all the cadre
        Trace tout les cadre
        """

        xStart = x
        for map in self.chargesMap:
            self.traceBasicCadre(xStart, map)
            EZ.trace_image(self.chargesMap[map], xStart + self.largeurCadre//2 - EZ.dimension(self.chargesMap[map])[0]//2, self.yDebutCadre + self.hauteurCardreInfo//2 - EZ.dimension(self.chargesMap[map])[1]//2)
            xStart += self.largeurCadrePlusEspace

    
    def displayMenu(self,x):
        """Display all the Menu
        Trace tout le Menu
        """

        self.displayFond()
        self.TraceWidget(x, self.chargesMap)
        self.traceAllCadre(x)
    
    def getMapName(self):
        """Return the name of the maps
        Retourne le nom des cartes"""

        return list(self.chargesMap.keys())


class Shop(Menu2Choice):
    """class to choice the shop
    class pour choisir le magasin"""

    def __init__(self, longeur, hauteur, texte):
        super().__init__(longeur, hauteur, texte)
        self.chargesBouton = [EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Shop\BoutonUpPlayer.png"), EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Shop\BoutonUpWeapon.png")]


class ShopUpgrade(SlideMenu):
    """class parent of slide Menu choice the character/Weapon in the shop
    class parent de SlideMenu pour choisir le personnage/arme dans le magasin"""

    def __init__(self, longeur, hauteur, texte, Inventaire = {}):
        super().__init__(longeur, hauteur, texte)
        self.hauteurCardreJoueur = int(3 * self.hauteurWidget/4)

        self.couleurFondCadre = (200, 200, 200)
        self.couleurBordureCadre = (150, 150, 150)

        self.policeCadre = EZ.charge_police(60, "FichiersJeu\Interface\Entites\Police\PermanentMarker-Regular.ttf", True)

        self.listPersonnage = [] # list of the character can be upgrade / liste des personnages pouvant etre ameliore



    
    def TrieInventaire(self, Inventaire):
        """sort iventory to return Caracters infomartion
        Trie Inventaire et renvoie les inforamtion sur les personnages

        Args:
            Inventaire (dict): dictionary of inventoty / dictionnaire de l'inventaire
        """

        Personnages = {}
        NumberCadre = 0
        for keys in Inventaire:
            if "Personnage" in keys:
                Personnages.update({keys: Inventaire[keys]})
                if Inventaire[keys][0]:
                    NumberCadre += 1
        
        self.infoPersonnages = Personnages

        self.largeurAllCadre = self.largeurCadrePlusEspace * NumberCadre

    def getListPersonnage(self):
        """Return the list of the character can be upgrade
        Retourne la liste des personnages pouvant etre ameliore"""
            
        return self.listPersonnage



    def traceCadreJoueur(self, x):
        """Draw the frame for Caracters
        Trace le Cadre des Personnages

        Args:
            x (int): x start of frame / x début du Cadre
        """

        Decor.traceCadre(x, self.yDebutCadre, self.largeurCadre, 3 *self.hauteurCardreJoueur//4, 3, 2, self.couleurFondCadre, self.couleurBordureCadre) # Haut du cadre
        Decor.traceCadre(x, self.yDebutCadre + 3 *self.hauteurCardreJoueur//4, 300, self.hauteurCardreJoueur//4, 3, 2, self.couleurBordureCadre, self.couleurBordureCadre) # Haut du cadre

        coordonneesFonts = [x + self.largeurCadre//2 - EZ.dimension(EZ.image_texte("Upgrade", self.policeCadre, 0, 0, 0))[0]//2, self.yDebutCadre + 7 *self.hauteurCardreJoueur//8 - EZ.dimension(EZ.image_texte("Select", self.policeCadre, 0, 0, 0))[1]//2] # [x, y]
        EZ.trace_image(EZ.image_texte("Upgrade", self.policeCadre, 0, 0, 0), coordonneesFonts[0] + self.tailleOmbrePolice , coordonneesFonts[1] + self.tailleOmbrePolice)
        EZ.trace_image(EZ.image_texte("Upgrade", self.policeCadre, 255, 255, 255), coordonneesFonts[0], coordonneesFonts[1])





    
    def traceMenuShopUpgrade(self, x, liste):
        """Drawn all the Menu of Caracters
        Trace tout le Menu des Personnages

        Args:
            x (int): x gap of widget / x du debut des Cadres
        """

        self.displayFond()
        self.TraceWidget(x, liste)


class ShopUpgradePersonnageSlide(ShopUpgrade):
    """Class of the slide menu for choice the character
    class du slide menu pour choisir le personnage"""

    def __init__(self, longeur, hauteur, texte, Inventaire={}):
        super().__init__(longeur, hauteur, texte, Inventaire)



    def traceAllPersonnages(self, x):
        """Drawn all the Caracters and their frames of buys characters
        Trace tout des personnages et leur cadre des personnages achetés

        Args:
            x (int): x start of frames / x du debut des Cadres
        """

        if self.chargesPersonnage == {}:
            self.chargePersonnage()

        listPersonnage = []
        xStart = x
        for infoPersonnage, ImagePeronnage in zip(self.infoPersonnages,self.chargesPersonnage):
            if self.infoPersonnages[infoPersonnage][0] == True:
                listPersonnage.append(infoPersonnage)
                self.traceCadreJoueur(xStart)
                EZ.trace_image(self.chargesPersonnage[ImagePeronnage], xStart + self.largeurCadre//2 - EZ.dimension(self.chargesPersonnage[ImagePeronnage])[0]//2, self.yDebutCadre + 20)
                xStart += self.largeurCadrePlusEspace
        
        self.listPersonnage = listPersonnage
    
    def traceMenuShopUpgrade(self, x):
        """Drawn all the Menu of Characters
        Trace tout le Menu des Personnages

        Args:
            x (int): x gap of widget / x du debut des Cadres
        """
        super().traceMenuShopUpgrade(x, self.listPersonnage)
        self.traceAllPersonnages(x)


class ShopUpgradeArmeSlide(ShopUpgrade):
    """Class of the slide menu for choice the weapon
    class du slide menu pour choisir l'arme"""

    def __init__(self, longeur, hauteur, texte, Inventaire={}):
        super().__init__(longeur, hauteur, texte, Inventaire)
        self.chargeWeapons() # dictionary of the weapons / dictionnaire des armes
        self.levelWeapons = {} # dictionary of the level of the weapons / dictionnaire des niveaux des armes
    
    def chargeWeapons(self):
        """Load the weapons
        Charge les armes"""

        sizeCoef = [150/(EZ.dimension(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme{n}\Arme{n}lvl1.png"))[1] if EZ.dimension(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme{n}\Arme{n}lvl1.png"))[0] * 150/EZ.dimension(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme{n}\Arme{n}lvl1.png"))[1] < self.largeurCadre else EZ.dimension(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme{n}\Arme{n}lvl1.png"))[0]//2) for n in range(1, 9)]

        self.chargesWeapons = {'Personnage1': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme1\Arme1lvl{n}.png"),0,sizeCoef[0])for n in range(1,5)],
                                'Personnage2': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme2\Arme2lvl{n}.png"),0,sizeCoef[1])for n in range(1,5)],
                                'Personnage3': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme3\Arme3lvl{n}.png"),0,sizeCoef[2])for n in range(1,4)],
                                'Personnage4': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme4\Arme4lvl{n}.png"),0,sizeCoef[3])for n in range(1,6)],
                                'Personnage5': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme5\Arme5lvl{n}.png"),0,sizeCoef[4])for n in range(1,5)],
                                'Personnage6': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme6\Arme6lvl{n}.png"),0,sizeCoef[5])for n in range(1,6)],
                                'Personnage7': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme7\Arme7lvl{n}.png"),0,sizeCoef[6])for n in range(1,6)],
                                'Personnage8': [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme8\Arme8lvl{n}.png"),0,sizeCoef[7])for n in range(1,5)],
        }
    
    def getNumberOfUpgrade(self, personnage):
        """Get the number of upgrade of the weapon
        Renvoie le nombre d'ameliorations de l'arme"""

        return len(self.chargesWeapons[personnage])

    
    def SetlevelWeapon(self):
        """Set the level of the weapons
        Met a niveau des armes"""

        Info = Reader.ReadInventaire()

        infotemp = {}
        for key, value in Info.items():
            infotemp.update({key: value[2]})
        
        self.levelWeapons = infotemp

        

    def traceAllWeapons(self, x):
        """Drawn all the weapons and their frames of buys weapons
        Trace toutes les armes et leur cadre des armes achetées

        Args:
            x (int): x start of frames / x du debut des Cadres
        """

        listArme = []
        xStart = x
        for infoPersonnage, ImageArme in zip(self.infoPersonnages,self.chargesWeapons):
            if self.infoPersonnages[infoPersonnage][0] == True:
                listArme.append(infoPersonnage)
                self.traceCadreJoueur(xStart)
                EZ.trace_image(self.chargesWeapons[ImageArme][self.levelWeapons[infoPersonnage] -1 ], xStart + self.largeurCadre//2 - EZ.dimension(self.chargesWeapons[ImageArme][self.levelWeapons[infoPersonnage] -1 ])[0]//2, self.yDebutCadre + self.hauteurCardreInfo//2 - EZ.dimension(self.chargesWeapons[ImageArme][self.levelWeapons[infoPersonnage] -1 ])[1]//2)
                xStart += self.largeurCadrePlusEspace
        
        self.listPersonnage = listArme

    def traceMenuShopUpgrade(self, x):
        """Drawn all the Menu of Weapons
        Trace tout le Menu des Armes"""

        super().traceMenuShopUpgrade(x, self.listPersonnage)
        self.traceAllWeapons(x)



class ShopUpgradePersonnage(StatsPersonnage):

    def __init__(self, longeur, hauteur, numPerso, texte, stats, statsUpgrade):
        super().__init__(longeur, hauteur, numPerso, texte, stats)
        self.statsUpgrade = statsUpgrade # Stats of the upgrade of the Characters / Stats de l'amelioration du personnage
        self.CaractersLevel = 1 # Level of the caracter / Niveau du personnage

        self.policeLevel = EZ.charge_police(40, "FichiersJeu\Interface\Entites\Police\PermanentMarker-Regular.ttf", True)

    def SetCarcatersLevel(self, CaractersLevel):
        """Set the level of the Caracters
        Set le niveau des personnages

        Args:
            CaractersLevel (int):level of Caracter / niveaux du personnage
        """
            
        self.CaractersLevel = CaractersLevel

    def traceCadreInfo(self):
        """Draw the stats of the Caracter
        Trace les stats du Personnage
        """
        
        for Cadre in range(1, 3):
            xCadre = Cadre * self.largeurWidget//2.5 - 150

            if Cadre == 1:
                # Caracters stats after the upgrade / Stats du personnage après amelioration
                EZ.trace_image(EZ.image_texte(f"Health: {int(self.stats['vie']) + int(self.statsUpgrade['vie']) * (self.CaractersLevel -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 10)
                EZ.trace_image(EZ.image_texte(f"Regen Time: {float(self.stats['regen']['cooldown']) + float(self.statsUpgrade['regen']['cooldown']) * (self.CaractersLevel -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 60)
                EZ.trace_image(EZ.image_texte(f"Regen Power: {round((float(self.stats['regen']['eficiency'])+ float(self.statsUpgrade['regen']['eficiency']) * (self.CaractersLevel -1)) * 10, 2)} ", self.policeCadre), xCadre + 10, self.yDebutCadre + 110)
                EZ.trace_image(EZ.image_texte(f"Speed: {int(self.stats['speed']) + float(self.statsUpgrade['speed']) * (self.CaractersLevel -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 160)
                EZ.trace_image(EZ.image_texte(f"Acc: {int(self.stats['acc']) + float(self.statsUpgrade['acc']) * (self.CaractersLevel -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 210)
                EZ.trace_image(EZ.image_texte(f"Jump Power: {float(self.stats['jumpPower']) + float(self.statsUpgrade['jumpPower']) * (self.CaractersLevel - 1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 260)


            elif Cadre == 2:
                # Caracters stats after the upgrade / Stats du personnage après amelioration
                EZ.trace_image(EZ.image_texte(f"Health: {int(self.stats['vie']) + int(self.statsUpgrade['vie']) * (self.CaractersLevel)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 10)
                EZ.trace_image(EZ.image_texte(f"Regen Time: {float(self.stats['regen']['cooldown']) + float(self.statsUpgrade['regen']['cooldown']) * (self.CaractersLevel)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 60)
                EZ.trace_image(EZ.image_texte(f"Regen Power: {round((float(self.stats['regen']['eficiency'])+ float(self.statsUpgrade['regen']['eficiency']) * (self.CaractersLevel)) * 10,2)} ", self.policeCadre), xCadre + 10, self.yDebutCadre + 110)
                EZ.trace_image(EZ.image_texte(f"Speed: {int(self.stats['speed']) + float(self.statsUpgrade['speed']) * (self.CaractersLevel)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 160)
                EZ.trace_image(EZ.image_texte(f"Acc: {int(self.stats['acc']) + float(self.statsUpgrade['acc']) * (self.CaractersLevel)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 210)
                EZ.trace_image(EZ.image_texte(f"Jump Power: {float(self.stats['jumpPower']) + float(self.statsUpgrade['jumpPower']) * (self.CaractersLevel)}", self.policeCadre), xCadre + 10, self.yDebutCadre + 260)
    

    def traceLevelCaracter(self):
        """Draw the level of the Caracter
        Trace le niveau du Personnage"""

        EZ.trace_image(EZ.image_texte(f"Level: {self.CaractersLevel}", self.policeLevel), self.largeurWidget//6 - EZ.dimension(EZ.image_texte(f"Level: {self.CaractersLevel}", self.policeLevel))[0]//2, self.yDebutCadre + 20)
    
    def tracePrix(self):
        """Draw the price of the Upgrade of the Caracters
        Trace le prix de l'amelioration du Personnage"""

        Decor.nombreDeGold(self.longeur - self.largeurWidget, self.yDebutWidget + self.hauteurWidget - 100, self.statsUpgrade['price']* self.CaractersLevel)
    
    def traceBouttonUp(self):
        """Draw the buy button
        Trace le bouton play
        """

        Btn.Bouton(self.largeurWidget - 250, self.yDebutWidget + self.hauteurWidget - 100, 250, 80, "Upgrade", (255, 255, 255), (0, 128, 64), 1, 3)

    def DisplayMenu(self):
        """Display the Menu of the Caracter
        Affiche le Menu du Personnage"""
        super().DisplayMenu()
        self.traceCadreInfo()
        self.traceLevelCaracter()
        self.tracePrix()
        self.traceBouttonUp()


class ShopUpgradeWeapon(StatsPersonnage):


    def __init__(self, longeur, hauteur, numPerso, texte, stats, statsUpgrade, numberOfWeaponUpgrade):
        super().__init__(longeur, hauteur, numPerso, texte, stats)
        self.statsUpgrade = statsUpgrade
        self.chargeWeapons(numberOfWeaponUpgrade)

    def SetWeaponLevel(self, level):
        """Set the weapon level
        Met le niveau de l'arme

        Args:
            level (int): level of the weapon
        """

        self.WeaponLevel = level


    def chargeWeapons(self,numbWeapon):
        """Load the weapons
        Charge les armes
        
        Args:
            numbWeapon (int): number of upgrade weapon / Nombre d'amelioration d'arme"""

        imageCoef = EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme{self.numPerso + 1}\Arme{self.numPerso + 1}lvl1.png")
        sizeCoef = 150/(EZ.dimension(imageCoef)[1] if EZ.dimension(imageCoef)[0] * 150/EZ.dimension(imageCoef)[1] < self.largeurCadre else EZ.dimension(imageCoef)[0]//2)
        self.chargesWeapons = [EZ.transforme_image(EZ.charge_image(f"FichiersJeu\Interface\Entites\Items\Arme\Arme{self.numPerso + 1}\Arme{self.numPerso + 1}lvl{n}.png"), 0, sizeCoef)for n in range(1,numbWeapon+1)]
        self.numbWeapon = numbWeapon



    def traceCadreInfo(self):
        """Draw the info of the weapon
        Trace les infos de l'arme"""

        for Cadre in range(1, 3):
            xCadre = Cadre * self.largeurWidget//2.5 - 150

            if Cadre == 1:
                # Picture of the weapon / Image de l'arme
                EZ.trace_image(self.chargesWeapons[self.WeaponLevel - 1], xCadre + self.largeurCadre//2 - EZ.dimension(self.chargesWeapons[self.WeaponLevel - 1])[0]//2, self.yDebutCadre + self.hauteurCardreInfo//4 - EZ.dimension(self.chargesWeapons[self.WeaponLevel - 1])[1]//2)

                # Weapon Stats / Stats de l'arme
                EZ.trace_image(EZ.image_texte(f"Damage: {self.stats['weapon']['damage'] + self.statsUpgrade['weapon']['damage'] * (self.WeaponLevel -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 160)
                EZ.trace_image(EZ.image_texte(f"Range: {self.stats['weapon']['range'] + self.statsUpgrade['weapon']['range'] * (self.WeaponLevel -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 110)
                EZ.trace_image(EZ.image_texte(f"Durability: {self.stats['weapon']['durability'] + self.statsUpgrade['weapon']['durability'] * (self.WeaponLevel -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 60)
            
            elif Cadre == 2:
                # Picture of the weapon / Image de l'arme
                self.WeaponLevel2 = self.WeaponLevel + 1 if self.WeaponLevel + 1 <= self.numbWeapon else self.WeaponLevel
                EZ.trace_image(self.chargesWeapons[self.WeaponLevel2 -1], xCadre + self.largeurCadre//2 - EZ.dimension(self.chargesWeapons[self.WeaponLevel2-1])[0]//2, self.yDebutCadre + self.hauteurCardreInfo//4 - EZ.dimension(self.chargesWeapons[self.WeaponLevel2 -1])[1]//2)

                # Weapon Stats / Stats de l'arme
                EZ.trace_image(EZ.image_texte(f"Damage: {self.stats['weapon']['damage'] + self.statsUpgrade['weapon']['damage'] * (self.WeaponLevel2 -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 160)
                EZ.trace_image(EZ.image_texte(f"Range: {self.stats['weapon']['range'] + self.statsUpgrade['weapon']['range'] * (self.WeaponLevel2 -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 110)
                EZ.trace_image(EZ.image_texte(f"Durability: {self.stats['weapon']['durability'] + self.statsUpgrade['weapon']['durability'] * (self.WeaponLevel2 -1)}", self.policeCadre), xCadre + 10, self.yDebutCadre + self.hauteurCardreInfo - 60)




    def tracePrix(self):
        """Draw the price of the Upgrade of the Caracters
        Trace le prix de l'amelioration du Personnage"""

        Decor.nombreDeGold(self.longeur - self.largeurWidget, self.yDebutWidget + self.hauteurWidget - 100, self.statsUpgrade['weapon']['price']* self.WeaponLevel if self.WeaponLevel < self.numbWeapon else 0)
    
    def traceBouttonUp(self):
        """Draw the buy button
        Trace le bouton play
        """

        Btn.Bouton(self.largeurWidget - 250, self.yDebutWidget + self.hauteurWidget - 100, 250, 80, "Upgrade" if self.WeaponLevel < self.numbWeapon else "Max", (255, 255, 255), (0, 128, 64), 1, 3)
    

    def DisplayMenu(self):
        """Display the Menu of the Weapon upgrade
        Affiche le Menu de l'amelioration d'arme"""
        super().DisplayMenu()
        self.traceCadreInfo()
        self.tracePrix()
        self.traceBouttonUp()



class BuyEquipement(SlideMenu):
    """Class to choice the equipement to buy
    class pour choisir l'équipement à acheter"""

    def __init__(self, longeur, hauteur, texte):
        super().__init__(longeur, hauteur, texte)
        self.largeurWidget = self.longeur - 100

        self.chargesEquipement = { "Shield": EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Equipement\Bouclier.png"), 
        "Grenade": EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Equipement\Grenade.png"),
        "Potion":EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Equipement\Potion.png"),
        }

        self.largeurAllCadre = self.largeurCadrePlusEspace * len(self.chargesEquipement)

    def traceAllCadre(self,x):
        """Draw all the cadre
        Trace tout les cadre
        """

        xStart = x
        for equipement in self.chargesEquipement:
            self.traceBasicCadre(xStart, equipement)
            EZ.trace_image(self.chargesEquipement[equipement], xStart + self.largeurCadre//2 - EZ.dimension(self.chargesEquipement[equipement])[0]//2, self.yDebutCadre + self.hauteurCardreInfo//2 - EZ.dimension(self.chargesEquipement[equipement])[1]//2)
            xStart += self.largeurCadrePlusEspace

    
    def displayMenu(self,x):
        """Display all the Menu
        Trace tout le Menu
        """

        self.displayFond()
        self.TraceWidget(x, self.chargesEquipement)
        self.traceAllCadre(x)


class InfoEquipement(SousMenu):
    """Class to display the info of the equipement
    class pour afficher les infos de l'équipement"""

    def __init__(self, longeur, hauteur, texte, equipement, equipementPicture, price):
        super().__init__(longeur, hauteur, texte)
        self.largeurWidget = self.longeur - 100
        self.hauteurCadre = int(2 * self.hauteurWidget/3)
        self.yDebutCadre = self.yDebutWidget + 50
        self.xDebutCadre = 100
        self.largeurCadreG = self.largeurWidget//2 # lenght of the right frame / longueur du cadre droit
        self.largeurCadreD = self.largeurWidget - 100 - self.largeurCadreG # lenght of the left frame / longueur du cadre gauche

        self.couleurBorderCadre = (140, 140, 140) # external color of frames info / Couleur externe des cadre info
        self.couleurFondCadre = (180, 180, 180) # Background color of frames info / Fond des cadre info

        self.equipement = equipement
        self.equipementPicture = equipementPicture
        self.price = price

        self.policeInfo = EZ.charge_police(25, "FichiersJeu\Interface\Entites\Police\Handwritingg _3.ttf")
        self.policeStats = EZ.charge_police(50, "FichiersJeu\Interface\Entites\Police\JosefinSans-BoldItalic.ttf")




    
    def traceCadreInfo(self):
        """Draw the cadre info
        Trace le cadre info """

        Decor.traceCadre(self.xDebutCadre, self.yDebutCadre, self.largeurCadreG, self.hauteurCadre, 2, 1,self.couleurFondCadre, self.couleurBorderCadre) # Drawn the left frame / Trace le cadre gauche
        Decor.traceCadre(self.xDebutCadre + self.largeurCadreG + 20, self.yDebutCadre, self.largeurCadreD, self.hauteurCadre, 2, 1,self.couleurFondCadre, self.couleurBorderCadre) # Drawn the right frame / Trace le cadre droit


    def traceEquipement(self):
        """Draw the equipement
        Trace l'équipement"""

        EZ.trace_image(self.equipementPicture, self.xDebutCadre + 10, self.yDebutCadre + self.hauteurCadre//2 - EZ.dimension(self.equipementPicture)[1]//2)
    

    def traceInfo(self):
        """Draw the info of the equipement
        Trace les infos de l'équipement"""

        # Description of the equipement / Description de l'équipement
        texte = {"Shield": "This shield is a basic shield.|It can be used to protect the|player from the enemy.| |You can see it's status,|in the top left corner in the game.| |It is automatically activated at|the beginning of the game|and at the end of the repair time.", 
                "Grenade": "This grenade is a powerful grenade.|It can be used to kill mob|and especially for the small monster|that the traditional weapon|does not touch .| |You can see it's status, in the|top left corner in the game.| |You can launch it with the 'e' key |in game.", 
                "Potion": "This potion is a heal potion.|It can be used to heal the player.| |You can see it's status, in the top|left corner in the game.| |You can drink it with the 'a' key |in game."}

        Decor.TraceTextArea(self.xDebutCadre + 40 + EZ.dimension(self.equipementPicture)[0], self.yDebutCadre + self.hauteurCadre//2 - EZ.dimension(self.equipementPicture)[1]//2, texte[self.equipement], self.policeInfo, (0, 0, 0))

        DECALAGE_HAUT = 80

        # Stats of the equipement / Stats de l'équipement
        StatsEquipement = Reader.ReadStatsEquipement()[self.equipement]
        if self.equipement == "Shield":
            EZ.trace_image(EZ.image_texte(f"Resistance: { StatsEquipement['eficiency']}",self.policeStats), self.xDebutCadre + self.largeurCadreG + 20 + self.largeurCadreD//2 - EZ.dimension(EZ.image_texte(f"Resistance: { StatsEquipement['eficiency']}",self.policeStats))[0]//2, self.yDebutCadre + DECALAGE_HAUT) 

        elif self.equipement == "Grenade":
            EZ.trace_image(EZ.image_texte(f"Damage: { StatsEquipement['eficiency']}",self.policeStats), self.xDebutCadre + self.largeurCadreG + 20 + self.largeurCadreD//2 - EZ.dimension(EZ.image_texte(f"Damage: { StatsEquipement['eficiency']}",self.policeStats))[0]//2, self.yDebutCadre + DECALAGE_HAUT)
            EZ.trace_image(EZ.image_texte(f"Range Bonus: { StatsEquipement['BonusRange']}",self.policeStats), self.xDebutCadre + self.largeurCadreG + 20 + self.largeurCadreD//2 - EZ.dimension(EZ.image_texte(f"Range Bonus: { StatsEquipement['BonusRange']}",self.policeStats))[0]//2, self.yDebutCadre + DECALAGE_HAUT + 2 * EZ.dimension(EZ.image_texte(f"Range Bonus: { StatsEquipement['BonusRange']}",self.policeStats))[1]//0.8)


        elif self.equipement == "Potion":
            EZ.trace_image(EZ.image_texte(f"Heal: { StatsEquipement['eficiency']}",self.policeStats), self.xDebutCadre + self.largeurCadreG + 20 + self.largeurCadreD//2 - EZ.dimension(EZ.image_texte(f"Heal: { StatsEquipement['eficiency']}",self.policeStats))[0]//2, self.yDebutCadre + DECALAGE_HAUT)
        
        # Other stats of the equipement / Autres stats de l'équipement
        EZ.trace_image(EZ.image_texte(f"Cooldown: { StatsEquipement['cooldown']}",self.policeStats), self.xDebutCadre + self.largeurCadreG + 20 + self.largeurCadreD//2 - EZ.dimension(EZ.image_texte(f"Cooldown: { StatsEquipement['cooldown']}",self.policeStats))[0]//2, self.yDebutCadre + DECALAGE_HAUT + EZ.dimension(EZ.image_texte(f"Heal: { StatsEquipement['eficiency']}",self.policeStats))[1]//0.8)
        



    
    def tracePrix(self):
        """Draw the price of the equipement
        Trace le prix de l'équipement"""
        if not(Reader.ReadEquipement()[self.equipement]):
            Decor.nombreDeGold(self.longeur - self.largeurWidget, self.yDebutWidget + self.hauteurWidget - 100, self.price )
        
        else:
            Btn.Bouton(self.longeur - self.largeurWidget, self.yDebutWidget + self.hauteurWidget - 100, 250, 80, "Upgrade", (255, 255, 255), (0, 128, 64), 1, 3)
    

    def traceBouttonBuy(self):
        """Draw the buy button
        Trace le bouton acheter"""

        Btn.Bouton(self.largeurWidget - 250, self.yDebutWidget + self.hauteurWidget - 100, 250, 80, "Buy" if not(Reader.ReadEquipement()[self.equipement]) else "Own", (255, 255, 255), (0, 128, 64), 1, 3)




    def DisplayMenu(self):
        """Display the Menu
        Trace le Menu"""

        self.displayFond()
        self.TraceWidget(self.largeurWidget)
        self.traceCadreInfo()
        self.traceEquipement()
        self.traceInfo()
        self.tracePrix()
        self.traceBouttonBuy()


class UgradeEquipement(SousMenu):
    """Upgrade the equipement
    Upgrade l'équipement"""

    def __init__(self, largeur, hauteur, equipement, equipementPicture, price):
        super().__init__(largeur, hauteur, equipement)
        self.largeurWidget = self.longeur - 100
        self.hauteurCadre = int(2 * self.hauteurWidget/5)
        self.hauteurCadre =  2 *self.hauteurCadre//3 if equipement == "Grenade" else self.hauteurCadre
        self.yDebutCadre = self.yDebutWidget + 50
        self.xDebutCadre = 100

        self.largeurCadre =  2 * self.largeurWidget//3 # Length of the frame / Longueur du cadre
        self.numberFrame = 2 # Number of frames / Nombre de cadres

        self.couleurBorderCadre = (140, 140, 140) # external color of frames info / Couleur externe des cadre info
        self.couleurFondCadre = (180, 180, 180) # Background color of frames info / Fond des cadre info

        self.equipement = equipement
        self.equipementPicture = equipementPicture
        self.price = price # price of the upgrade / Prix de l'amélioration → Prix de l'équipement/2 * number of upgrade

        self.policeStats = EZ.charge_police(70, "FichiersJeu\Interface\Entites\Police\JosefinSans-BoldItalic.ttf")


    def traceCadreInfo(self):
        """Draw the cadre info
        Trace le cadre info """

        if self.equipement == "Grenade":
            self.numberFrame = 3
        
        else:
            self.numberFrame = 2

        for cadre in range(self.numberFrame):
            Decor.traceCadre(self.xDebutCadre + 270, self.yDebutCadre + cadre * self.hauteurCadre//0.9, self.largeurCadre, self.hauteurCadre, 2, 1,self.couleurFondCadre, self.couleurBorderCadre) # Drawn the frames / Trace les cadres
            Decor.traceFlecheAmelioration(int(self.xDebutCadre + 840), int(self.yDebutCadre + cadre * self.hauteurCadre//0.9 + self.hauteurCadre//2 - 60), 1.2) # Drawn the arrow / Trace les flèches (60 = 80(height arrow) * 1.5(zoom)/2)
            

    def traceInfo(self):
        """Draw the info of the equipement
        Trace les infos de l'équipement"""
        StatsEquipement = Reader.ReadStatsEquipement()[self.equipement]

        if self.equipement == "Grenade":
            EZ.trace_image(EZ.image_texte(f"Bonus :",self.policeStats), self.xDebutCadre + 290, self.yDebutCadre + 2 * self.hauteurCadre//0.9 + self.hauteurCadre//2 - EZ.dimension(EZ.image_texte(f"Bonus Range : { StatsEquipement['BonusRange']} → {int(StatsEquipement['BonusRange'] + 10 )}",self.policeStats))[1]//2)
            EZ.trace_image(EZ.image_texte(f"{ StatsEquipement['BonusRange']}   →   {int(StatsEquipement['BonusRange'] + 10)}",self.policeStats), self.xDebutCadre + 290 + self.largeurCadre - 40 - EZ.dimension(EZ.image_texte(f"{ StatsEquipement['BonusRange']}   →   {int(StatsEquipement['BonusRange'] + 10)}",self.policeStats))[0], self.yDebutCadre + 2 * self.hauteurCadre//0.9 + self.hauteurCadre//2 - EZ.dimension(EZ.image_texte(f"Bonus Range : { StatsEquipement['BonusRange']} → {int(StatsEquipement['BonusRange'] * 0.9)}",self.policeStats))[1]//2)

        EZ.trace_image(EZ.image_texte("Damage :" if self.equipement == "Grenade" else "Heal" if self.equipement == "Potion" else "Resistance"  ,self.policeStats), self.xDebutCadre + 290, self.yDebutCadre + self.hauteurCadre//2 - EZ.dimension(EZ.image_texte(f"Damage : { StatsEquipement['eficiency']} → {round(StatsEquipement['eficiency'] * 1.2,2)}",self.policeStats))[1]//2)
        EZ.trace_image(EZ.image_texte(f"{ StatsEquipement['eficiency']}   →   {round(StatsEquipement['eficiency'] * 1.1,1) if len(str(int(StatsEquipement['eficiency']))) < 2 and not(self.equipement == 'Shield') else round(StatsEquipement['eficiency'] * 1.1) if not(self.equipement == 'Shield') else StatsEquipement['eficiency'] + 1 }",self.policeStats), self.xDebutCadre + 290 + self.largeurCadre - 40 - EZ.dimension(EZ.image_texte(f"{ StatsEquipement['eficiency']}   →   {round(StatsEquipement['eficiency'] * 1.2,1) if len(str(int(StatsEquipement['eficiency']))) < 2 else round(StatsEquipement['eficiency'] * 1.2)}",self.policeStats))[0], self.yDebutCadre + self.hauteurCadre//2 - EZ.dimension(EZ.image_texte(f"Bonus Range : { StatsEquipement['BonusRange']} → {int(StatsEquipement['BonusRange'] * 0.9)}",self.policeStats))[1]//2)
        

        EZ.trace_image(EZ.image_texte(f"Cooldown : ",self.policeStats), self.xDebutCadre + 290, self.yDebutCadre + self.hauteurCadre//0.9 + self.hauteurCadre//2 - EZ.dimension(EZ.image_texte(f"Cooldown : { StatsEquipement['cooldown']} → {int(StatsEquipement['cooldown'] * 0.9)}",self.policeStats))[1]//2)
        EZ.trace_image(EZ.image_texte(f"{ StatsEquipement['cooldown']}   →   {int(StatsEquipement['cooldown'] * 0.9)}",self.policeStats), self.xDebutCadre + 290 + self.largeurCadre - 40 - EZ.dimension(EZ.image_texte(f"{ StatsEquipement['cooldown']}   →   {int(StatsEquipement['cooldown'] * 0.9)}",self.policeStats))[0], self.yDebutCadre + self.hauteurCadre//0.9 + self.hauteurCadre//2 - EZ.dimension(EZ.image_texte(f"Bonus Range : { StatsEquipement['BonusRange']} → {int(StatsEquipement['BonusRange'] * 0.9)}",self.policeStats))[1]//2)

    def traceEquipement(self):
        """Draw the equipement
        Trace l'équipement"""

        EZ.trace_image(self.equipementPicture, self.xDebutCadre + 10, self.yDebutWidget + self.hauteurWidget//2 - EZ.dimension(self.equipementPicture)[1]//2)

    def traceBouttonUp(self):
        """Draw the buy button
        Trace le bouton acheter"""

        for cadre in range(self.numberFrame):
            Btn.Bouton_Vertical(self.xDebutCadre + 270 + self.largeurCadre,  self.yDebutCadre + cadre * self.hauteurCadre//0.9, 50, self.hauteurCadre, "UP", (255, 255, 255), (0, 128, 64), 1, 3, 50)
    
    def tracePrix(self):
        """Draw the price of the equipement
        Trace le prix de l'équipement"""

        Decor.nombreDeGold(self.longeur - self.largeurWidget, self.yDebutWidget + self.hauteurWidget - 100, self.price * Reader.ReadStatsEquipement()[self.equipement]['numberUpgrade'])





    def DisplayMenu(self):
        """Display the Menu
        Trace le Menu"""

        self.displayFond()
        self.TraceWidget(self.largeurWidget)
        self.traceBouttonUp()
        self.traceCadreInfo()
        self.traceEquipement()
        self.traceInfo()
        self.tracePrix()


class MenuMap(Menu):
    """Class to display the map of the menu mode campagne
    Class pour afficher la map du menu mode campagne"""

    def __init__(self, longeur, hauteur,zoomMap):
        super().__init__(longeur, hauteur)
        self.zoomMap = zoomMap
        self.chargeMap() # load the map / charge la map
        self.coordonnerBoutonMonde = {"Terre": [670 * self.zoomMap,3950 * self.zoomMap],
        "Mars": [1270 * self.zoomMap,2650 * self.zoomMap],
        "Gluton": [755 * self.zoomMap,1285 * self.zoomMap],
        "Volcano": [2015 * self.zoomMap,315 * self.zoomMap],
        "Forestia": [3550 * self.zoomMap,1330 * self.zoomMap],
        "Dead Zone": [3335 * self.zoomMap,2815 * self.zoomMap],
        "Candya": [3680 * self.zoomMap,4167 * self.zoomMap],} # Coordinates of the buttons / Coordonnées des boutons [x,y]

        self.tailleBoutonMonde = [930 * self.zoomMap,510 * self.zoomMap] # Size of the buttons / Taille des boutons [l,h]
    
    def chargeMap(self):
        """load the map
        Charge la map"""

        self.map = EZ.transforme_image(EZ.charge_image("FichiersJeu\Interface\Entites\Items\ImageInterface\Mode\CartesSpaceShooter.png"),0,self.zoomMap)
    
    def getCoordonnerBouton(self):
        """Get the coordinates of buttons
        Renvoie les coordonnées des boutons"""

        return self.coordonnerBoutonMonde
    
    def getTailleBouton(self):
        """Get the size of the button
        Renvoie la taille du bouton"""

        return self.tailleBoutonMonde
    
    def getTailleFond(self):
        """Get the size of the background
        Renvoie la taille du fond"""

        return EZ.dimension(self.map)
    
    def displayFond(self,x,y):
        """Display the background
        Affiche le fond"""

        EZ.trace_image(self.map, x, y)



class Game(Interface):
    """Class to display the Game and manage it
    Classe pour afficher le jeu et le gérer"""

    def __init__(self, longeur, hauteur):
        super().__init__(longeur, hauteur)

        self.chargesFond = None
        self.decal = 0 # decalage de l'image 2
        self.decalage = 0     # decalage effectué
        self.CoordonnerFictive = 0 # Calcule le decalage total depuis le debut de la Game pour crée une impression de coordoner dans une map

        self.move_info = {"right": False, "left": False, "saut": False, "inertie": 0}
        self.move_possible = {"right": True, "left": True}  #Donne les deplacement que le joueur peux effectuer (permet d'interfire certain deplacement)
        self.contact = False

        self.map = "Mars"
        self.largeurFond = 3000 # map width / Largeur de la map
        self.hauteurSol = 604 # ground height / Hauteur du sol

    def setMap(self, map):
        """Set the map
        Defini la map"""
        self.map = map
        self.chargeFond()

    def chargeFond(self):
        """ Load the background image
        Charge l'image du fond"""

        if self.map == "Terre":
            self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Terre.jpg")
            self.largeurFond = 5000
            self.hauteurSol = 620

        elif self.map == "Mars":
            self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Mars.png")
            self.largeurFond = 2040
            self.hauteurSol = 604
        
        elif self.map == "Gluton":
            self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Gluton.jpg")
            self.largeurFond = 2967
            self.hauteurSol = 630

        elif self.map == "Volcano":
            self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Volcano.jpg")
            self.largeurFond = 2545
            self.hauteurSol = 620
    
        elif self.map == "Forestia":
            self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Forestia.jpg")
            self.largeurFond = 2687
            self.hauteurSol = 630
    
        elif self.map == "Dead Zone":
            self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\DeadZone.jpg")
            self.largeurFond = 3000
            self.hauteurSol = 615

        elif self.map == "Candya":
            self.chargesFond = EZ.charge_image("FichiersJeu\Interface\Entites\Fond\FondMap\Candya.jpg")
            self.largeurFond = 3000
            self.hauteurSol = 620



    def displayFond(self, acc, vitesse):
        """ display the background image
        Trace le fond du jeu"""


        if self.chargesFond == None:
            self.chargeFond()
        
        self.move(acc,vitesse)

        while not(0 <= self.decal <= self.largeurFond):
            if self.decal > self.largeurFond:
                self.decal -= self.largeurFond

            elif self.decal < 0:
                self.decal += self.largeurFond
        

        decal_x = [self.decal - self.largeurFond, self.decal]

        for fond in range(2):
            EZ.trace_image(self.chargesFond ,decal_x[fond],0)


        
    

    def move(self, acc, vitesse):
        """Move the background image for give on the player a movement
        Deplace l'image du fond pour donner au joueur un mouvement"""

        if not(self.contact):
            if not(self.move_info["saut"]):

                if self.move_info["right"] == True:
                    if (self.decalage + acc) <= vitesse:
                        self.decalage += acc
                    
                    elif self.decalage > vitesse:
                        self.decalage -= 1
                    

                
                elif self.move_info["left"] == True:
                    if (self.decalage - acc) >= -vitesse:
                        self.decalage -= acc

                    elif self.decalage < -vitesse:
                        self.decalage += 1

                else:
                    # vitesse de d'arret

                    # Gauche
                    if self.decalage < -1:
                        self.decalage += 1

                    elif self.decalage < 0:
                        self.decalage -= self.decalage

                    # Droite
                    elif self.decalage > 1:
                        self.decalage -= 1 

                    elif self.decalage > 0:
                        self.decalage -= self.decalage
                        




            else:
                if self.move_info["right"] == True:
                    if (self.decalage + acc * 0.5) <= vitesse * 1.1:
                        self.decalage += acc * 0.5
                    

                
                elif self.move_info["left"] == True:
                    if (self.decalage - acc * 0.5) >= -vitesse * 1.1:
                        self.decalage -= acc * 0.5
                
            

        else: # Si le joueur est en contacte d'un objet

            if self.move_info["right"] and self.move_possible["right"] and self.decalage >= 0:
                if (self.decalage + acc) <= vitesse:
                    self.decalage += acc
                
                elif self.decalage > vitesse:
                    self.decalage -= 1
                

            
            elif self.move_info["left"] and self.move_possible["left"] and self.decalage <= 0:
                if (self.decalage - acc) >= -vitesse:
                    self.decalage -= acc

                elif self.decalage < -vitesse:
                    self.decalage += 1

            else:
                self.decalage = 0


        self.decal -= self.decalage # Le fond bouge dans le sens inverse
        self.CoordonnerFictive += self.decalage
    
    def saveNumeroVague(self, numero):
        """Save the number of the wave
        sauvegarde le numero de la vague"""

        self.numVague = Decor.saveNumberRoman(numero, (200,200,200))
    
    def displayNumeroVague(self):
        """Display the number of the wave
        Affiche le numero de la vague"""

        X = self.longeur - self.longeur//4
        Y = 20

        if self.numVague != None:
            Decor.traceCadre(X, Y, 204, 50, 2, 0, (200,200,200), (0,0,0))
            EZ.trace_image(self.numVague, X + 2, Y + 2)
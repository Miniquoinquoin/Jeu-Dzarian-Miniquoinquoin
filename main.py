"""Fichier principale du projet"""

import FichiersJeu.Interface.EZ as EZ
# import FichiersJeu.Joueur.CaracteristiqueJoueur as CJ
# import FichiersJeu.Interface.Entites.Menu as Menuf
import FichiersJeu.InterfaceDynamique as ID

#Csv
import FichiersJeu.InfoJoueur.ReadInfo as Reader
import FichiersJeu.InfoJoueur.SaveInfo as Writer

HAUTEUR = 720
LONGEUR = 1280

EZ.creation_fenetre(LONGEUR, HAUTEUR, "Prototype 1")

def Shooter():
    gold = int(Reader.ReadGold())
    inventaire = Reader.ReadInventaire()


    demande = ID.menu(gold, inventaire)
    play = True
    while play:

        if demande == "Menu":
            demande = ID.menu(gold, inventaire)
            
        if demande == "Game":
            demande, tmpGold = ID.game()
            gold += tmpGold
            tmpGold = 0

        if not(demande):
            Writer.Save(gold, inventaire)
            break

Shooter()

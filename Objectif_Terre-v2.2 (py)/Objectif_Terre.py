#-------------------------------------------------------------------------------
# Name:        Objectif_Terre
# Purpose:     Lancement du logiciel Objectif_Terre
#
# Author:      Guillaume Lebegue / Theo Duval
#-------------------------------------------------------------------------------

##Importation des modules necessaires-------------------------------------------
from tkinter import *
import Core.Bin.ModulePrincipale
import Core.Bin.ModuleInterface as ModuleInterface
import pygame.mixer as mixer
import pygame.mixer_music as music

##Main--------------------------------------------------------------------------
def main():
    pass
if __name__ == '__main__':
    main()

    mixer.init() #Initialisation du module de son
    chemson="Core/Son/" #Chemin des fichier sonores

    #Blibliotheque de son
        #Son de test
    blibliBruit={} #Creation d'une blibliotheque de son

    sonChenille=mixer.Sound(chemson+"352588__humanoidefilms__umbrella-opening-slow.wav") #Creation du son
    sonChenille.set_volume(0.5)
    blibliBruit["sonChenille"]=sonChenille #Ajout du son a la blibliotheque

    chute=mixer.Sound(chemson+"159408__noirenex__life-lost-game-over.wav") #Creation du son
    chute.set_volume(0.8)
    blibliBruit["chute"]=chute #Ajout du son a la blibliotheque

    blibliSon={} #Blibliotheque generale
    blibliSon["Bruit"]=blibliBruit #Ajout de la blibliotheque secondaire

    music.load(chemson+"397089__timbre__remix-of-erokia-s-freesound-394011.wav")
    music.set_volume(0.5)

    fen = Tk() #Creation fenetre
    fen.resizable(False, False) #Empeche redefinition fenetre
    fen.title("Objectif Terre")

    #Creation des in terfaces
    interface1=ModuleInterface.InterfaceAcceuil(fen,blibliSon)
    interface2=ModuleInterface.InterfaceNiveau1(fen,blibliSon)
    interface3=ModuleInterface.InterfaceNiveau2(fen,blibliSon)
    interface4=ModuleInterface.InterfaceNiveau3(fen,blibliSon)
    interface5=ModuleInterface.InterfaceNiveau4(fen,blibliSon)
    interface6=ModuleInterface.InterfaceSauvegarde(fen,blibliSon)
    interface7=ModuleInterface.InterfaceManuelDutilisation(fen,blibliSon)
    interface8=ModuleInterface.InterfaceMappeur(fen,blibliSon)

    #Liaison des interfaces entre elles
    interface1.interfaceSuiv=interface6
    interface1.interfaceManuel=interface7
    interface1.interfaceMappeur=interface8

    interface2.interface1=interface1
    interface2.interface2=interface2
    interface2.interface3=interface3
    interface2.interface4=interface4
    interface2.interface5=interface5
    interface2.interface6=interface6

    interface3.interface1=interface1
    interface3.interface2=interface2
    interface3.interface3=interface3
    interface3.interface4=interface4
    interface3.interface5=interface5
    interface3.interface6=interface6

    interface4.interface1=interface1
    interface4.interface2=interface2
    interface4.interface3=interface3
    interface4.interface4=interface4
    interface4.interface5=interface5
    interface4.interface6=interface6

    interface5.interface1=interface1
    interface5.interface2=interface2
    interface5.interface3=interface3
    interface5.interface4=interface4
    interface5.interface5=interface5
    interface5.interface6=interface6

    interface6.interface1=interface1
    interface6.interface2=interface2
    interface6.interface3=interface3
    interface6.interface4=interface4
    interface6.interface5=interface5

    interface7.interfaceAcceuil=interface1

    interface8.interfaceAcceuil=interface1

    music.play(-1)

    #Lancement
    fen.mainloop()

    music.stop()

#-------------------------------------------------------------------------------
# Name:        Mappeur
# Purpose:     Lance le mappeur du logiciel Objectif_Terre
#
# Author:      Guillaume Lebegue
#
# Copyright:   (c) ikkino 2018
#-------------------------------------------------------------------------------

##Iportation des modules necessaires--------------------------------------------
import Core.Bin.ModuleMappeur
from tkinter import *

##Main--------------------------------------------------------------------------
def main():
    pass
if __name__ == '__main__':
    main()

    fenetre=Tk() #Fenetre principale
    fenetre.title("Mappeur") #Titre de la fenetre
    fenetre.resizable(False,False) #Empeche modification taille fenetre

    blibliSon={}

    interface=Core.Bin.ModuleMappeur.Interface(fenetre,blibliSon,"",) #Charge l'interface

    interface.mainloop() #Lance la fenetre
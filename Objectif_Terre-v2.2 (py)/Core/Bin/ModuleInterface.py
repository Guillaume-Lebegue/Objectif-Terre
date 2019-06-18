#-------------------------------------------------------------------------------
# Name:        ModuleInterface
# Purpose:     Module de class concernant l'interface du logiciel Objectif_Terre
#
# Author:      Theo Duval
#-------------------------------------------------------------------------------

##Importation des modules necessaires-------------------------------------------
from tkinter import*
from tkinter.messagebox import *
import os
import Core.Bin.ModulePrincipale  as ModulePrincipale
import pickle
import pygame.mixer_music as music
import Core.Bin.ModuleMappeur as ModuleMappeur

#Chemin des images de l'interface
chemin="Core/Ressources/Interface/"
chemin1='Core/Ressources/Interface/manuel/'

##Class--------------------------------------------------------------------------
class InterfaceAcceuil(Frame):
    def __init__(self, fenetre,bliblison, **kwargs):
        self.fenetre=fenetre
        self.bliblison=bliblison
        Frame.__init__(self,self.fenetre, width=1000, height=650)
        self.pack()
        self.pack_propagate(0)
        self.canvas = Canvas(self, bg='black', width=1000, height=650)
        self.canvas.pack()

        self.interfaceSuiv=Frame

        self.fond= PhotoImage(file=chemin+'fond_accueil_v6.gif')   #image de fond
        self.canvas.create_image(500,325, image=self.fond)

        self.ImageBouton1= PhotoImage(file=chemin+'BoutonJouer.gif')       #bouton jouer
        self.BoutonJouer = Button(self,image=self.ImageBouton1,width=180,height=80,borderwidth=0,highlightthickness=0,command=self.MenuJouer)
        self.BoutonJouer["bg"]="black"
        self.BoutonJouer["fg"]="white"
        self.BoutonJouer.place(x=200,y=200)

        self.ImageBouton3= PhotoImage(file=chemin+'BoutonMappeur.gif')           #Bouton Mappeur
        self.BoutonRegles = Button(self, image=self.ImageBouton3,width=180, height=80,borderwidth=0,highlightthickness=0, command=self.MenuMappeur )
        self.BoutonRegles["bg"]="black"
        self.BoutonRegles["fg"]="white"
        self.BoutonRegles.place(x=450,y=200)

        self.ImageBouton2= PhotoImage(file=chemin+'BoutonManuel.gif')           #Bouton regle
        self.BoutonRegles = Button(self, image=self.ImageBouton2,width=180, height=80,borderwidth=0,highlightthickness=0, command=self.Manuel)
        self.BoutonRegles["bg"]="black"
        self.BoutonRegles["fg"]="white"
        self.BoutonRegles.place(x=700,y=200)


        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

    def MenuJouer(self):
        self.pack_forget()
        self.interfaceSuiv.pack()

    def Manuel(self):
        self.pack_forget()
        self.interfaceManuel.pack()

    def MenuMappeur(self):
        self.pack_forget()
        self.interfaceMappeur.pack()


class InterfaceMappeur(Frame):
    def __init__(self,fenetre,bliblison):
        self.fenetre=fenetre
        self.bliblison=bliblison
        self.mapACharge=""
        Frame.__init__(self,self.fenetre, width=1000, height=650)
        self.pack_propagate(0)
        self.canvas = Canvas(self, bg='black', width=1000, height=650)
        self.canvas.pack()

        self.interfaceAcceuil=Frame

        self.fond= PhotoImage(file=chemin+'fond_accueil_v6.gif')   #image de fond
        self.canvas.create_image(500,325, image=self.fond)


        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

        self.ImageBouton5= PhotoImage(file=chemin+'BoutonRetour.gif')           #Bouton retour
        self.BoutonRetour = Button(self, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.FonctionRetour)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.ImageBouton1= PhotoImage(file=chemin+'BoutonJouer.gif')       #bouton jouer
        self.BoutonJouer = Button(self,image=self.ImageBouton1,width=180,height=80,borderwidth=0,highlightthickness=0,command=self.FonctionJouer)
        self.BoutonJouer["bg"]="black"
        self.BoutonJouer["fg"]="white"
        self.BoutonJouer.place(x=410,y=200)

        self.ImageBouton3= PhotoImage(file=chemin+'BoutonMappeur.gif')           #Bouton Mappeur
        self.BoutonMappeur = Button(self, image=self.ImageBouton3,width=180, height=80,borderwidth=0,highlightthickness=0,command=self.FonctionMappeur)
        self.BoutonMappeur["bg"]="black"
        self.BoutonMappeur["fg"]="white"
        self.BoutonMappeur.place(x=410,y=300)

    def FonctionRetour(self):
        self.pack_forget()
        self.interfaceAcceuil.pack()

    def FonctionMappeur(self):
        self.pack_forget()
        mappeur=ModuleMappeur.Interface(self.fenetre,self.bliblison,self)

    def FonctionJouer(self):
        charge=SelectNiveau(self)
        if self.mapACharge != "":
            self.pack_forget()
            music.fadeout(100)
            music.load("Core/Son/427452__sirkoto51__atmospheric-ambiance-loop-3.wav")
            music.set_volume(0.2)
            music.play(-1)
            niveau=ModulePrincipale.Niveau(self.fenetre,self.mapACharge,self,1,1)
            self.mapACharge=""
        else:
            showinfo("Selection","Vous n'avez pas selectionner de niveau")

    def Suite(self,result,nbNiveau=""):
        if result == 0:
            self.fenetre.destroy()
        else:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            self.pack()


class SelectNiveau(Toplevel):
    def __init__(self,parent):
        self.parent=parent
        Toplevel.__init__(self)
        self.listeFichMap = os.listdir('Carte-Cree')
        if self.listeFichMap != []: #Si la liste de fichier n'est pas vide
            self.frameMap = Frame(self) #Frame principale de la fenetre
            self.frameMap.pack()

            self.listeMap = Listbox(self.frameMap) #Boite de selection de carte
            self.listeMap.pack()

            for carte in self.listeFichMap: #Pour chaque carte dans la liste
                self.listeMap.insert(END, carte) #Ajout a la boite de selection

            self.listeMap.selection_set( first = 0 ) #Selection par defaut

            self.boutonOk = Button(self.frameMap, text='Select', command=self.Select) #Bouton ok liee a la methode Select
            self.boutonOk.pack(fill=X)

            self.protocol("WM_DELETE_WINDOW", self.Select) #Fermeture de la fenetre = fonction Select
            self.transient() #Declare fenetre secondaire
            self.grab_set()
            self.focus_set() #Focus de l'ecran
            self.wait_window() #Gele le reste du programe
        else:
            showerror("Aucune carte","Aucune carte n'a ete trouve") #Fenetre du module tkinter.messageBox
            self.destroy()

    def Select(self):
        """Fonction de la class FenetreCharge
        Recupere la selection et l'enregistre
        """
        self.parent.mapACharge = self.listeMap.get(self.listeMap.curselection()) #Recupere la selection et la modifie sur le parent
        self.destroy() #Ferme la fenetre

class InterfaceManuelDutilisation(Frame):
    def __init__(self,fenetre,bliblison,):
        self.fenetre=fenetre
        self.bliblison=bliblison
        Frame.__init__(self,self.fenetre, width=1000, height=650, bg='black')
        self.pack_propagate(0)

        self.interfaceAcceuil=Frame


        self.fond = PhotoImage(file=chemin+'fond manuel d utilisation.gif')   #image de fond
        self.ImageBouton5= PhotoImage(file=chemin+'BoutonRetour.gif')           #Bouton retour


#######################

        self.frameAcceuilManuel=Canvas(self,width=1000,height=650)
        self.frameAcceuilManuel.place(x=0,y=0)
        self.frameAcceuilManuel.create_image(500,325, image=self.fond)

        self.ImageManuelRobot= PhotoImage(file=chemin1+'robot.gif')           #Bouton manuel robot
        self.BoutonManuelRobot = Button(self.frameAcceuilManuel, image=self.ImageManuelRobot,width=180, height=80,borderwidth=0,highlightthickness=0, command=self.RobotMAnuel )
        self.BoutonManuelRobot["bg"]="black"
        self.BoutonManuelRobot["fg"]="white"
        self.BoutonManuelRobot.place(x=450,y=200)

        self.ImageManuelTerrain= PhotoImage(file=chemin1+'terrain.gif')           #Bouton manuel terrain
        self.BoutonManuelTerrain = Button(self.frameAcceuilManuel, image=self.ImageManuelTerrain,width=180, height=80,borderwidth=0,highlightthickness=0, command=self.TerrainManuel )
        self.BoutonManuelTerrain["bg"]="black"
        self.BoutonManuelTerrain["fg"]="white"
        self.BoutonManuelTerrain.place(x=450,y=300)

        self.ImageManuelAction= PhotoImage(file=chemin1+'action.gif')           #Bouton manuel action
        self.BoutonManuelAction = Button(self.frameAcceuilManuel, image=self.ImageManuelAction,width=180, height=80,borderwidth=0,highlightthickness=0, command=self.ActionManuel )
        self.BoutonManuelAction["bg"]="black"
        self.BoutonManuelAction["fg"]="white"
        self.BoutonManuelAction.place(x=450,y=400)

        self.BoutonRetour = Button(self.frameAcceuilManuel, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.FonctionRetour)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)


#########################

        self.frameRobotManuel=Canvas(self,width=1000,height=650)
        self.frameRobotManuel.create_image(500,325, image=self.fond)

        self.ImageGrandRobot= PhotoImage(file=chemin1+'grand_robot.gif',master=self)    # Image grand robot
        self.grand_robot=Canvas(self.frameRobotManuel ,width=200,height=300,borderwidth=0,highlightthickness=0)
        self.grand_robot.create_image(100,150,image=self.ImageGrandRobot)
        self.grand_robot.place(x=100,y=150)

        self.ImageMiniRrobot= PhotoImage(file=chemin1+'mini_robot.gif',master=self)    # Image mini robot
        self.mini_robot=Canvas(self.frameRobotManuel,width=36,height=36,borderwidth=0,highlightthickness=0)
        self.mini_robot.create_image(18,18,image=self.ImageMiniRrobot)
        self.mini_robot.place(x=350,y=150)

        self.ImageRobot= PhotoImage(file=chemin1+'texte robot.gif',master=self)    # Image Texte Robot
        self.ImageRobot1=Canvas(self.frameRobotManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageRobot1.create_image(250,25,image=self.ImageRobot)
        self.ImageRobot1.place(x=350,y=290)

        self.BoutonRetour = Button(self.frameRobotManuel,borderwidth=0,highlightthickness=0, image=self.ImageBouton5,width=90, height=40, command=self.AcceuilManuel)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)


############################

        self.frameTerrainManuel=Canvas(self,width=1000,height=650)
        self.frameTerrainManuel.create_image(500,325, image=self.fond)

        self.ImageDepart= PhotoImage(file=chemin1+'Start.gif',master=self)    # Image case depard
        self.case_depart=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_depart.create_image(25,25,image=self.ImageDepart)
        self.case_depart.place(x=25,y=110)

        self.ImageTexteDepart= PhotoImage(file=chemin1+'texte depart.gif',master=self)    # Image Texte Depart
        self.ImageTexteDepart1=Canvas(self.frameTerrainManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteDepart1.create_image(250,25,image=self.ImageTexteDepart)
        self.ImageTexteDepart1.place(x=85,y=110)

        self.ImageArriver= PhotoImage(file=chemin1+'End.gif',master=self)    # Image case arriver
        self.case_arriver=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_arriver.create_image(25,25,image=self.ImageArriver)
        self.case_arriver.place(x=25,y=170)

        self.ImageTexteArriver= PhotoImage(file=chemin1+'texte arriver.gif',master=self)    # Image Texte Arriver
        self.ImageTexteArriver1=Canvas(self.frameTerrainManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteArriver1.create_image(250,25,image=self.ImageTexteArriver)
        self.ImageTexteArriver1.place(x=85,y=170)

        self.ImageSol= PhotoImage(file=chemin1+'sol.gif',master=self)    # Image case sol
        self.case_sol=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_sol.create_image(25,25,image=self.ImageSol)
        self.case_sol.place(x=25,y=230)

        self.ImageTexteSol= PhotoImage(file=chemin1+'texte sol.gif',master=self)    # Image Texte sol
        self.ImageTexteSol1=Canvas(self.frameTerrainManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteSol1.create_image(250,25,image=self.ImageTexteSol)
        self.ImageTexteSol1.place(x=85,y=230)

        self.ImageVide= PhotoImage(file=chemin1+'vide.gif',master=self)    # Image case vide
        self.case_vide=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_vide.create_image(25,25,image=self.ImageVide)
        self.case_vide.place(x=25,y=290)

        self.ImageTexteVide= PhotoImage(file=chemin1+'terrain vide.gif',master=self)    # Image Texte vide
        self.ImageTexteVide1=Canvas(self.frameTerrainManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteVide1.create_image(250,25,image=self.ImageTexteVide)
        self.ImageTexteVide1.place(x=85,y=290)

        self.ImageBarriere1= PhotoImage(file=chemin1+'Barriere.gif',master=self)    # Image case barierre 1
        self.case_barriere1=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_barriere1.create_image(25,25,image=self.ImageBarriere1)
        self.case_barriere1.place(x=25,y=350)

        self.ImageBarriere2= PhotoImage(file=chemin1+'Croix_Barriere.gif',master=self)    # Image case barierre 2
        self.case_barriere2=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_barriere2.create_image(25,25,image=self.ImageBarriere2)
        self.case_barriere2.place(x=85,y=350)

        self.ImageTextebarierre= PhotoImage(file=chemin1+'terrain barierre.gif',master=self)    # Image Texte barierre
        self.ImageTextebarierre1=Canvas(self.frameTerrainManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTextebarierre1.create_image(250,25,image=self.ImageTextebarierre)
        self.ImageTextebarierre1.place(x=145,y=350)

        self.ImagePontOuvert= PhotoImage(file=chemin1+'pont_ouvert.gif',master=self)    # Image case pont ouvert
        self.case_pont_ouvert=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_pont_ouvert.create_image(25,25,image=self.ImagePontOuvert)
        self.case_pont_ouvert.place(x=25,y=410)

        self.ImageTextePontOuvert= PhotoImage(file=chemin1+'texte pont ouvert.gif',master=self)    # Image Texte pont ouvert
        self.ImageTextePontOuvert1=Canvas(self.frameTerrainManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTextePontOuvert1.create_image(250,25,image=self.ImageTextePontOuvert)
        self.ImageTextePontOuvert1.place(x=85,y=410)

        self.ImagePontFermer= PhotoImage(file=chemin1+'pont_fermer.gif',master=self)    # Image case pont ouvert
        self.case_pont_fermer=Canvas(self.frameTerrainManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_pont_fermer.create_image(25,25,image=self.ImagePontFermer)
        self.case_pont_fermer.place(x=25,y=470)

        self.ImageTextePontFermer= PhotoImage(file=chemin1+'texte pont fermer.gif',master=self)    # Image Texte pont fermer
        self.ImageTextePontFermer1=Canvas(self.frameTerrainManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTextePontFermer1.create_image(250,25,image=self.ImageTextePontFermer)
        self.ImageTextePontFermer1.place(x=85,y=470)

        self.ImageSuivant2= PhotoImage(file=chemin1+'retour2.gif')           #Bouton aller page 2
        self.BoutonSuivant2 = Button(self.frameTerrainManuel, image=self.ImageSuivant2,width=45, height=45, command=self.Suivant2 )
        self.BoutonSuivant2["bg"]="black"
        self.BoutonSuivant2["fg"]="white"
        self.BoutonSuivant2.place(x=475,y=580)

        self.BoutonRetour = Button(self.frameTerrainManuel, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.AcceuilManuel)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

        ######

        self.frameTerrainManuel2=Canvas(self,width=1000,height=650)
        self.frameTerrainManuel2.create_image(500,325, image=self.fond)

        self.ImageBoutonON= PhotoImage(file=chemin1+'bouton_ON.gif',master=self)    # Image case bouton on
        self.case_bouton_ON=Canvas(self.frameTerrainManuel2,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_bouton_ON.create_image(25,25,image=self.ImageBoutonON)
        self.case_bouton_ON.place(x=25,y=110)

        self.ImageBoutonOFF= PhotoImage(file=chemin1+'bouton_OFF.gif',master=self)    # Image case bouton off
        self.case_bouton_OFF=Canvas(self.frameTerrainManuel2,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_bouton_OFF.create_image(25,25,image=self.ImageBoutonOFF)
        self.case_bouton_OFF.place(x=85,y=110)

        self.ImageTexteBouton= PhotoImage(file=chemin1+'texte bouton.gif',master=self)    # Image Texte bouton
        self.ImageTexteBouton1=Canvas(self.frameTerrainManuel2,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteBouton1.create_image(250,25,image=self.ImageTexteBouton)
        self.ImageTexteBouton1.place(x=145,y=110)

        self.ImageBoite= PhotoImage(file=chemin1+'Case_Poser_Boite.gif',master=self)    # Image case boite
        self.case_Poser_Boite=Canvas(self.frameTerrainManuel2,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_Poser_Boite.create_image(25,25,image=self.ImageBoite)
        self.case_Poser_Boite.place(x=25,y=170)

        self.ImageTextePlateformeBoite= PhotoImage(file=chemin1+'texte boite.gif',master=self)    # Image Texte plateforme boite
        self.ImageTextePlateformeBoite1=Canvas(self.frameTerrainManuel2,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTextePlateformeBoite1.create_image(250,25,image=self.ImageTextePlateformeBoite)
        self.ImageTextePlateformeBoite1.place(x=85,y=170)

        self.ImageBoutonBoite= PhotoImage(file=chemin1+'Case_Bouton_Boite.gif',master=self)    # Image case bouton boite
        self.case_Bouton_Boite=Canvas(self.frameTerrainManuel2,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.case_Bouton_Boite.create_image(25,25,image=self.ImageBoutonBoite)
        self.case_Bouton_Boite.place(x=25,y=230)

        self.ImageTexteBoite= PhotoImage(file=chemin1+'texte bouton boite.gif',master=self)    # Image Texte bouton boite
        self.ImageTexteBoite1=Canvas(self.frameTerrainManuel2,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteBoite1.create_image(250,25,image=self.ImageTexteBoite)
        self.ImageTexteBoite1.place(x=85,y=230)

        self.ImageSuivant1= PhotoImage(file=chemin1+'retour1.gif')           #Bouton aller page 2
        self.BoutonSuivant1 = Button(self.frameTerrainManuel2, image=self.ImageSuivant1,width=50, height=50, borderwidth=0,highlightthickness=0, command=self.Suivant1 )
        self.BoutonSuivant1["bg"]="black"
        self.BoutonSuivant1["fg"]="white"
        self.BoutonSuivant1.place(x=475,y=580)

        self.BoutonRetour = Button(self.frameTerrainManuel2, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.AcceuilManuel)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

#############################

        self.frameActionManuel=Canvas(self,width=1000,height=650)
        self.frameActionManuel.create_image(500,325, image=self.fond)

        self.ImageActionAvancer= PhotoImage(file=chemin1+'Fleche_Avancer.gif',master=self)    # Image fleche avancer
        self.action_avancer=Canvas(self.frameActionManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.action_avancer.create_image(25,25,image=self.ImageActionAvancer)
        self.action_avancer.place(x=25,y=110)

        self.ImageTexteAvancer= PhotoImage(file=chemin1+'texte Avancer.gif',master=self)    # Image texte fleche avancer
        self.ImageTexteAvancer1=Canvas(self.frameActionManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteAvancer1.create_image(250,25,image=self.ImageTexteAvancer)
        self.ImageTexteAvancer1.place(x=85,y=110)

        self.ImageActionTounerDroit= PhotoImage(file=chemin1+'Fleche_Touner_Droit.gif',master=self)    # Image fleche tourner drtoit
        self.action_touner_droit=Canvas(self.frameActionManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.action_touner_droit.create_image(25,25,image=self.ImageActionTounerDroit)
        self.action_touner_droit.place(x=25,y=170)

        self.ImageTexteTounerDroit= PhotoImage(file=chemin1+'texte tourner droit.gif',master=self)    # Image texte fleche touner droit
        self.ImageTexteTounerDroit1=Canvas(self.frameActionManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteTounerDroit1.create_image(250,25,image=self.ImageTexteTounerDroit)
        self.ImageTexteTounerDroit1.place(x=85,y=170)

        self.ImageActionTounerGauche= PhotoImage(file=chemin1+'Fleche_Touner_Gauche.gif',master=self)    # Image fleche tourner gauche
        self.action_touner_gauche=Canvas(self.frameActionManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.action_touner_gauche.create_image(25,25,image=self.ImageActionTounerGauche)
        self.action_touner_gauche.place(x=25,y=230)

        self.ImageTexteTounerGauche= PhotoImage(file=chemin1+'texte tourner gauche.gif',master=self)    # Image texte fleche touner gauche
        self.ImageTexteTounerGauche1=Canvas(self.frameActionManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTexteTounerGauche1.create_image(250,25,image=self.ImageTexteTounerGauche)
        self.ImageTexteTounerGauche1.place(x=85,y=230)

        self.ImageActionPrendre= PhotoImage(file=chemin1+'Fleche_Prendre.gif',master=self)    # Image fleche tourner gauche
        self.action_prendre=Canvas(self.frameActionManuel,width=50,height=50,borderwidth=0,highlightthickness=0)
        self.action_prendre.create_image(25,25,image=self.ImageActionPrendre)
        self.action_prendre.place(x=25,y=290)

        self.ImageTextePrendre= PhotoImage(file=chemin1+'texte poser boite.gif',master=self)    # Image texte fleche touner gauche
        self.ImageTextePrendre1=Canvas(self.frameActionManuel,width=500,height=50,borderwidth=0,highlightthickness=0)
        self.ImageTextePrendre1.create_image(250,25,image=self.ImageTextePrendre)
        self.ImageTextePrendre1.place(x=85,y=290)

        self.BoutonRetour = Button(self.frameActionManuel, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.AcceuilManuel)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)


    def AcceuilManuel(self):

        self.frameRobotManuel.place_forget()
        self.frameTerrainManuel.place_forget()
        self.frameTerrainManuel2.place_forget()
        self.frameActionManuel.place_forget()
        self.frameAcceuilManuel.pack()


    def RobotMAnuel(self):

        self.frameAcceuilManuel.place_forget()
        self.frameRobotManuel.place(x=0,y=0)


    def TerrainManuel(self):

        self.frameAcceuilManuel.place_forget()
        self.frameTerrainManuel.place(x=0,y=0)

    def ActionManuel(self):
        self.frameAcceuilManuel.place_forget()
        self.frameActionManuel.place(x=0,y=0)


    def FonctionRetour(self):
        self.pack_forget()
        self.interfaceAcceuil.pack()

    def Suivant2(self):

        self.frameTerrainManuel.place_forget()
        self.frameTerrainManuel2.place(x=0,y=0)

    def Suivant1(self):

        self.frameTerrainManuel2.place_forget()
        self.frameTerrainManuel.place(x=0,y=0)







class InterfaceSauvegarde(Frame):
    def __init__(self,fenetre,bliblison):
        self.fenetre=fenetre
        self.bliblison=bliblison
        Frame.__init__(self,self.fenetre, width=1000, height=650)
        self.pack_propagate(0)
        self.canvas = Canvas(self, bg='black', width=1000, height=650)
        self.canvas.pack()

        self.interface1=Frame
        self.interface2=Frame
        self.interface3=Frame
        self.interface4=Frame
        self.interface5=Frame
        self.interface6=Frame

        self.fond= PhotoImage(file=chemin+'fond_accueil_v6.gif')   #image de fond
        self.canvas.create_image(500,325, image=self.fond)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

        self.ImageBouton5= PhotoImage(file=chemin+'BoutonRetour.gif')           #Bouton retour
        self.BoutonRetour = Button(self, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.FonctionRetour)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.ImageBoutonSave1= PhotoImage(file=chemin+'BoutonSauvegarde1.gif')           #Bouton save 1
        self.BoutonSave1 = Button(self, image=self.ImageBoutonSave1,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda: self.FonctionLancerSave("1",1))
        self.BoutonSave1["bg"]="black"
        self.BoutonSave1["fg"]="white"
        self.BoutonSave1.place(x=230,y=200)

        self.ImageBoutonSave2= PhotoImage(file=chemin+'BoutonSauvegarde2.gif')           #Bouton save 2
        self.BoutonSave2 = Button(self, image=self.ImageBoutonSave2,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda: self.FonctionLancerSave("2",1))
        self.BoutonSave2["bg"]="black"
        self.BoutonSave2["fg"]="white"
        self.BoutonSave2.place(x=430,y=200)

        self.ImageBoutonSave3= PhotoImage(file=chemin+'BoutonSauvegarde3.gif')           #Bouton save 3
        self.BoutonSave3 = Button(self, image=self.ImageBoutonSave3,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda: self.FonctionLancerSave("3",1))
        self.BoutonSave3["bg"]="black"
        self.BoutonSave3["fg"]="white"
        self.BoutonSave3.place(x=630,y=200)

    def FonctionRetour(self):
        self.pack_forget()
        self.interface1.pack()

    def FonctionLancerSave(self,save,mode=0):
        self.pack_forget()
        self.save=save
        with open("Core/Save/{}".format(save), 'rb') as fichier: #Utilisation du module pickle
            depickler = pickle.Unpickler(fichier)
            nbDebloque = depickler.load() #Chargement du fichier
        nbDebloque=int(nbDebloque)

        if nbDebloque < 20:
            self.interface5.BoutonNiveau20.config(state='disabled')
        else:
            self.interface5.BoutonNiveau20.config(state='normal')

        if nbDebloque < 19:
            self.interface5.BoutonNiveau19.config(state='disabled')
        else:
            self.interface5.BoutonNiveau19.config(state='normal')

        if nbDebloque < 18:
            self.interface5.BoutonNiveau18.config(state='disabled')
        else:
            self.interface5.BoutonNiveau18.config(state='normal')

        if nbDebloque < 17:
            self.interface5.BoutonNiveau17.config(state='disabled')
        else:
            self.interface5.BoutonNiveau17.config(state='normal')

        if nbDebloque < 16:
            self.interface5.BoutonNiveau16.config(state='disabled')
        else:
            self.interface5.BoutonNiveau16.config(state='normal')

        if nbDebloque < 15:
            self.interface4.BoutonNiveau15.config(state='disabled')
        else:
            self.interface4.BoutonNiveau15.config(state='normal')

        if nbDebloque < 14:
            self.interface4.BoutonNiveau14.config(state='disabled')
        else:
            self.interface4.BoutonNiveau14.config(state='normal')

        if nbDebloque < 13:
            self.interface4.BoutonNiveau13.config(state='disabled')
        else:
            self.interface4.BoutonNiveau13.config(state='normal')

        if nbDebloque < 12:
            self.interface4.BoutonNiveau12.config(state='disabled')
        else:
            self.interface4.BoutonNiveau12.config(state='normal')

        if nbDebloque < 11:
            self.interface4.BoutonNiveau11.config(state='disabled')
        else:
            self.interface4.BoutonNiveau11.config(state='normal')

        if nbDebloque < 10:
            self.interface3.BoutonNiveau10.config(state='disabled')
        else:
            self.interface3.BoutonNiveau10.config(state='normal')

        if nbDebloque < 9:
            self.interface3.BoutonNiveau9.config(state='disabled')
        else:
            self.interface3.BoutonNiveau9.config(state='normal')

        if nbDebloque < 8:
            self.interface3.BoutonNiveau8.config(state='disabled')
        else:
            self.interface3.BoutonNiveau8.config(state='normal')

        if nbDebloque < 7:
            self.interface3.BoutonNiveau7.config(state='disabled')
        else:
            self.interface3.BoutonNiveau7.config(state='normal')

        if nbDebloque < 6:
            self.interface3.BoutonNiveau6.config(state='disabled')
        else:
            self.interface3.BoutonNiveau6.config(state='normal')

        if nbDebloque < 5:
            self.interface2.BoutonNiveau5.config(state='disabled')
        else:
            self.interface2.BoutonNiveau5.config(state='normal')

        if nbDebloque < 4:
            self.interface2.BoutonNiveau4.config(state='disabled')
        else:
            self.interface2.BoutonNiveau4.config(state='normal')

        if nbDebloque < 3:
            self.interface2.BoutonNiveau3.config(state='disabled')
        else:
            self.interface2.BoutonNiveau3.config(state='normal')

        if nbDebloque < 2:
            self.interface2.BoutonNiveau2.config(state='disabled')
        else:
            self.interface2.BoutonNiveau2.config(state='normal')

        if mode == 1:
            self.interface2.pack()


class InterfaceNiveau1(Frame):
    def __init__(self,fenetre,bliblison):
        self.fenetre=fenetre
        self.bliblison=bliblison
        Frame.__init__(self,self.fenetre, width=1000, height=650)
        self.pack_propagate(0)
        self.canvas = Canvas(self, bg='black', width=1000, height=650)
        self.canvas.pack()

        self.interface1=Frame
        self.interface2=Frame
        self.interface3=Frame
        self.interface4=Frame
        self.interface5=Frame
        self.interface6=Frame

        self.fond= PhotoImage(file=chemin+'fondniveaua.gif')   #image de fond
        self.canvas.create_image(500,325, image=self.fond)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

        self.ImageBouton5= PhotoImage(file=chemin+'BoutonRetour.gif')           #Bouton retour
        self.BoutonRetour = Button(self, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.FonctionRetour)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.ImageNiveau1= PhotoImage(file=chemin+'niveau1.gif')           #Bouton Niveau 1
        self.BoutonNiveau1 = Button(self, image=self.ImageNiveau1,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("01",0))
        self.BoutonNiveau1["bg"]="black"
        self.BoutonNiveau1["fg"]="white"
        self.BoutonNiveau1.place(x=247,y=406)

        self.ImageNiveau2= PhotoImage(file=chemin+'niveau2.gif')           #Bouton Niveau 2
        self.BoutonNiveau2 = Button(self, image=self.ImageNiveau2,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("02",0))
        self.BoutonNiveau2["bg"]="black"
        self.BoutonNiveau2["fg"]="white"
        self.BoutonNiveau2.place(x=665,y=448)

        self.ImageNiveau3= PhotoImage(file=chemin+'niveau3.gif')           #Bouton Niveau 3
        self.BoutonNiveau3 = Button(self, image=self.ImageNiveau3,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("03",0))
        self.BoutonNiveau3["bg"]="black"
        self.BoutonNiveau3["fg"]="white"
        self.BoutonNiveau3.place(x=485,y=302)

        self.ImageNiveau4= PhotoImage(file=chemin+'niveau4.gif')           #Bouton Niveau 4
        self.BoutonNiveau4 = Button(self, image=self.ImageNiveau4,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("04",0))
        self.BoutonNiveau4["bg"]="black"
        self.BoutonNiveau4["fg"]="white"
        self.BoutonNiveau4.place(x=279,y=100)

        self.ImageNiveau5= PhotoImage(file=chemin+'niveau5.gif')           #Bouton Niveau 5
        self.BoutonNiveau5 = Button(self, image=self.ImageNiveau5,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("05",0))
        self.BoutonNiveau5["bg"]="black"
        self.BoutonNiveau5["fg"]="white"
        self.BoutonNiveau5.place(x=640,y=133)

        self.ImageRetour1= PhotoImage(file=chemin+'retour1.gif')           #Bouton Retour Niveau 1
        self.BoutonRetour1 = Button(self, image=self.ImageRetour1,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau1 )
        self.BoutonRetour1["bg"]="black"
        self.BoutonRetour1["fg"]="white"
        self.BoutonRetour1.place(x=318,y=572)

        self.ImageRetour2= PhotoImage(file=chemin+'retour2.gif')           #Bouton Retour Niveau 2
        self.BoutonRetour2 = Button(self, image=self.ImageRetour2,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau2 )
        self.BoutonRetour2["bg"]="black"
        self.BoutonRetour2["fg"]="white"
        self.BoutonRetour2.place(x=415,y=572)

        self.ImageRetour3= PhotoImage(file=chemin+'retour3.gif')           #Bouton Retour Niveau 3
        self.BoutonRetour3 = Button(self, image=self.ImageRetour3,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau3 )
        self.BoutonRetour3["bg"]="black"
        self.BoutonRetour3["fg"]="white"
        self.BoutonRetour3.place(x=515,y=572)

        self.ImageRetour4= PhotoImage(file=chemin+'retour4.gif')           #Bouton Retour Niveau 4
        self.BoutonRetour4 = Button(self, image=self.ImageRetour4,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau4)
        self.BoutonRetour4["bg"]="black"
        self.BoutonRetour4["fg"]="white"
        self.BoutonRetour4.place(x=615,y=572)

        self.ImageReset= PhotoImage(file=chemin+'reset.gif')
        self.BoutonReset= Button(self, image=self.ImageReset, width=50, height=50,borderwidth=0,highlightthickness=0, command=self.Reinitialiser)
        self.BoutonReset["bg"]="black"
        self.BoutonReset["fg"]="white"
        self.BoutonReset.place(x=70,y=572)

    def FonctionRetour(self):
        self.pack_forget()
        self.interface1.pack()

    def FonctionRetourNiveau1(self):
        self.pack_forget()
        self.interface2.pack()

    def FonctionRetourNiveau2(self):
        self.pack_forget()
        self.interface3.pack()

    def FonctionRetourNiveau3(self):
        self.pack_forget()
        self.interface4.pack()

    def FonctionRetourNiveau4(self):
        self.pack_forget()
        self.interface5.pack()

    def Lancer(self,nb,mode=1):
        self.pack_forget()
        music.fadeout(100)
        music.load("Core/Son/427452__sirkoto51__atmospheric-ambiance-loop-3.wav")
        music.set_volume(0.2)
        music.play(-1)
        niveau=ModulePrincipale.Niveau(self.fenetre,nb,self,mode)

    def Suite(self,result,nbNiveau=""):
        if result == 1:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            self.pack()
        elif result == 0:
            self.fenetre.destroy()
        elif result == 2:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            with open("Core/Save/{}".format(self.interface6.save), 'rb') as fichier: #Utilisation du module pickle
                depickler = pickle.Unpickler(fichier)
                nbDebloque = depickler.load() #Chargement du fichier

            if int(nbDebloque)==int(nbNiveau):
                if int(nbNiveau) <10:
                    nbDebloque = "0"+str(int(nbNiveau)+1)
                elif int(nbNiveau) <20:
                    nbDebloque = str(int(nbNiveau)+1)
                else:
                    nbDebloque=nbNiveau

                with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                    pickler = pickle.Pickler(fichier)
                    pickler.dump(nbDebloque) #Enregistrement

            self.interface6.FonctionLancerSave(self.interface6.save)
            self.pack()

    def Reinitialiser(self):
        if askyesno("Reinitialiser ?","Voulez-vous reinitialiser la sauvegarde ? \n(Cette action est irreversible)"):
            if self.interface6.save == "1":
                nbDebloque="20"
            else:
                nbDebloque="01"
            with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                pickler = pickle.Pickler(fichier)
                pickler.dump(nbDebloque) #Enregistrement
            showinfo("Reinitialisation","Reinitialisation reussi !")
            self.interface6.FonctionLancerSave(self.interface6.save)


class InterfaceNiveau2(Frame):
    def __init__(self,fenetre,bliblison):
        self.fenetre=fenetre
        self.bliblison=bliblison
        Frame.__init__(self,self.fenetre, width=1000, height=650)
        self.pack_propagate(0)
        self.canvas = Canvas(self, bg='black', width=1000, height=650)
        self.canvas.pack()

        self.interface1=Frame
        self.interface2=Frame
        self.interface3=Frame
        self.interface4=Frame
        self.interface5=Frame
        self.interface6=Frame

        self.fond= PhotoImage(file=chemin+'fondniveaua.gif')   #image de fond
        self.canvas.create_image(500,325, image=self.fond)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

        self.ImageBouton5= PhotoImage(file=chemin+'BoutonRetour.gif')           #Bouton retour
        self.BoutonRetour = Button(self, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.FonctionRetour)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.ImageNiveau6= PhotoImage(file=chemin+'niveau6.gif')           #Bouton Niveau 6
        self.BoutonNiveau6 = Button(self, image=self.ImageNiveau6,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("06",0))
        self.BoutonNiveau6["bg"]="black"
        self.BoutonNiveau6["fg"]="white"
        self.BoutonNiveau6.place(x=247,y=406)

        self.ImageNiveau7= PhotoImage(file=chemin+'niveau7.gif')           #Bouton Niveau 7
        self.BoutonNiveau7 = Button(self, image=self.ImageNiveau7,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("07",0))
        self.BoutonNiveau7["bg"]="black"
        self.BoutonNiveau7["fg"]="white"
        self.BoutonNiveau7.place(x=665,y=448)

        self.ImageNiveau8= PhotoImage(file=chemin+'niveau8.gif')           #Bouton Niveau 8
        self.BoutonNiveau8 = Button(self, image=self.ImageNiveau8,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("08",0))
        self.BoutonNiveau8["bg"]="black"
        self.BoutonNiveau8["fg"]="white"
        self.BoutonNiveau8.place(x=485,y=302)

        self.ImageNiveau9= PhotoImage(file=chemin+'niveau9.gif')           #Bouton Niveau 9
        self.BoutonNiveau9 = Button(self, image=self.ImageNiveau9,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("09",0))
        self.BoutonNiveau9["bg"]="black"
        self.BoutonNiveau9["fg"]="white"
        self.BoutonNiveau9.place(x=279,y=100)

        self.ImageNiveau10= PhotoImage(file=chemin+'niveau10.gif')           #Bouton Niveau 10
        self.BoutonNiveau10 = Button(self, image=self.ImageNiveau10,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("10"))
        self.BoutonNiveau10["bg"]="black"
        self.BoutonNiveau10["fg"]="white"
        self.BoutonNiveau10.place(x=640,y=133)

        self.ImageRetour1= PhotoImage(file=chemin+'retour1.gif')           #Bouton Retour Niveau 1
        self.BoutonRetour1 = Button(self, image=self.ImageRetour1,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau1 )
        self.BoutonRetour1["bg"]="black"
        self.BoutonRetour1["fg"]="white"
        self.BoutonRetour1.place(x=318,y=572)

        self.ImageRetour2= PhotoImage(file=chemin+'retour2.gif')           #Bouton Retour Niveau 2
        self.BoutonRetour2 = Button(self, image=self.ImageRetour2,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau2 )
        self.BoutonRetour2["bg"]="black"
        self.BoutonRetour2["fg"]="white"
        self.BoutonRetour2.place(x=415,y=572)

        self.ImageRetour3= PhotoImage(file=chemin+'retour3.gif')           #Bouton Retour Niveau 3
        self.BoutonRetour3 = Button(self, image=self.ImageRetour3,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau3 )
        self.BoutonRetour3["bg"]="black"
        self.BoutonRetour3["fg"]="white"
        self.BoutonRetour3.place(x=515,y=572)

        self.ImageRetour4= PhotoImage(file=chemin+'retour4.gif')           #Bouton Retour Niveau 4
        self.BoutonRetour4 = Button(self, image=self.ImageRetour4,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau4 )
        self.BoutonRetour4["bg"]="black"
        self.BoutonRetour4["fg"]="white"
        self.BoutonRetour4.place(x=615,y=572)

        self.ImageReset= PhotoImage(file=chemin+'reset.gif')
        self.BoutonReset= Button(self, image=self.ImageReset,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.Reinitialiser)
        self.BoutonReset["bg"]="black"
        self.BoutonReset["fg"]="white"
        self.BoutonReset.place(x=70,y=572)

    def FonctionRetour(self):
        self.pack_forget()
        self.interface1.pack()

    def FonctionRetourNiveau1(self):
        self.pack_forget()
        self.interface2.pack()

    def FonctionRetourNiveau2(self):
        self.pack_forget()
        self.interface3.pack()

    def FonctionRetourNiveau3(self):
        self.pack_forget()
        self.interface4.pack()

    def FonctionRetourNiveau4(self):
        self.pack_forget()
        self.interface5.pack()

    def Lancer(self,nb,mode=1):
        self.pack_forget()
        music.fadeout(100)
        music.load("Core/Son/427452__sirkoto51__atmospheric-ambiance-loop-3.wav")
        music.set_volume(0.2)
        music.play(-1)
        niveau=ModulePrincipale.Niveau(self.fenetre,nb,self,mode)

    def Suite(self,result,nbNiveau=""):
        if result == 1:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            self.pack()
        elif result == 0:
            self.fenetre.destroy()
        elif result == 2:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            with open("Core/Save/{}".format(self.interface6.save), 'rb') as fichier: #Utilisation du module pickle
                depickler = pickle.Unpickler(fichier)
                nbDebloque = depickler.load() #Chargement du fichier

            if int(nbDebloque)==int(nbNiveau):
                if int(nbNiveau) <10:
                    nbDebloque = "0"+str(int(nbNiveau)+1)
                elif int(nbNiveau) <20:
                    nbDebloque = str(int(nbNiveau)+1)
                else:
                    nbDebloque=nbNiveau

                with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                    pickler = pickle.Pickler(fichier)
                    pickler.dump(nbDebloque) #Enregistrement

            self.interface6.FonctionLancerSave(self.interface6.save)
            self.pack()

    def Reinitialiser(self):
        if askyesno("Reinitialiser ?","Voulez-vous reinitialiser la sauvegarde ? \n(Cette action est irreversible)"):
            if self.interface6.save == "1":
                nbDebloque="20"
            else:
                nbDebloque="01"
            with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                pickler = pickle.Pickler(fichier)
                pickler.dump(nbDebloque) #Enregistrement
            showinfo("Reinitialisation","Reinitialisation reussi !")
            self.interface6.FonctionLancerSave(self.interface6.save)


class InterfaceNiveau3(Frame):
    def __init__(self,fenetre,bliblison):
        self.fenetre=fenetre
        self.bliblison=bliblison
        Frame.__init__(self,self.fenetre, width=1000, height=650)
        self.pack_propagate(0)
        self.canvas = Canvas(self, bg='black', width=1000, height=650)
        self.canvas.pack()

        self.interface1=Frame
        self.interface2=Frame
        self.interface3=Frame
        self.interface4=Frame
        self.interface5=Frame
        self.interface6=Frame

        self.fond= PhotoImage(file=chemin+'fondniveaua.gif')   #image de fond
        self.canvas.create_image(500,325, image=self.fond)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

        self.ImageBouton5= PhotoImage(file=chemin+'BoutonRetour.gif')           #Bouton retour
        self.BoutonRetour = Button(self, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.FonctionRetour)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.ImageNiveau11= PhotoImage(file=chemin+'niveau11.gif')           #Bouton Niveau 11
        self.BoutonNiveau11 = Button(self, image=self.ImageNiveau11,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("11") )
        self.BoutonNiveau11["bg"]="black"
        self.BoutonNiveau11["fg"]="white"
        self.BoutonNiveau11.place(x=247,y=406)

        self.ImageNiveau12= PhotoImage(file=chemin+'niveau12.gif')           #Bouton Niveau 12
        self.BoutonNiveau12 = Button(self, image=self.ImageNiveau12,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("12"))
        self.BoutonNiveau12["bg"]="black"
        self.BoutonNiveau12["fg"]="white"
        self.BoutonNiveau12.place(x=665,y=448)

        self.ImageNiveau13= PhotoImage(file=chemin+'niveau13.gif')           #Bouton Niveau 13
        self.BoutonNiveau13 = Button(self, image=self.ImageNiveau13,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("13"))
        self.BoutonNiveau13["bg"]="black"
        self.BoutonNiveau13["fg"]="white"
        self.BoutonNiveau13.place(x=485,y=302)

        self.ImageNiveau14= PhotoImage(file=chemin+'niveau14.gif')           #Bouton Niveau 14
        self.BoutonNiveau14 = Button(self, image=self.ImageNiveau14,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("14"))
        self.BoutonNiveau14["bg"]="black"
        self.BoutonNiveau14["fg"]="white"
        self.BoutonNiveau14.place(x=279,y=100)

        self.ImageNiveau15= PhotoImage(file=chemin+'niveau15.gif')           #Bouton Niveau 15
        self.BoutonNiveau15 = Button(self, image=self.ImageNiveau15,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("15"))
        self.BoutonNiveau15["bg"]="black"
        self.BoutonNiveau15["fg"]="white"
        self.BoutonNiveau15.place(x=640,y=133)

        self.ImageRetour1= PhotoImage(file=chemin+'retour1.gif')           #Bouton Retour Niveau 1
        self.BoutonRetour1 = Button(self, image=self.ImageRetour1,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau1 )
        self.BoutonRetour1["bg"]="black"
        self.BoutonRetour1["fg"]="white"
        self.BoutonRetour1.place(x=318,y=572)

        self.ImageRetour2= PhotoImage(file=chemin+'retour2.gif')           #Bouton Retour Niveau 2
        self.BoutonRetour2 = Button(self, image=self.ImageRetour2,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau2 )
        self.BoutonRetour2["bg"]="black"
        self.BoutonRetour2["fg"]="white"
        self.BoutonRetour2.place(x=415,y=572)

        self.ImageRetour3= PhotoImage(file=chemin+'retour3.gif')           #Bouton Retour Niveau 3
        self.BoutonRetour3 = Button(self, image=self.ImageRetour3,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau3 )
        self.BoutonRetour3["bg"]="black"
        self.BoutonRetour3["fg"]="white"
        self.BoutonRetour3.place(x=515,y=572)

        self.ImageRetour4= PhotoImage(file=chemin+'retour4.gif')           #Bouton Retour Niveau 4
        self.BoutonRetour4 = Button(self, image=self.ImageRetour4,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau4 )
        self.BoutonRetour4["bg"]="black"
        self.BoutonRetour4["fg"]="white"
        self.BoutonRetour4.place(x=615,y=572)

        self.ImageReset= PhotoImage(file=chemin+'reset.gif')
        self.BoutonReset= Button(self, image=self.ImageReset, width=50, height=50,borderwidth=0,highlightthickness=0, command=self.Reinitialiser)
        self.BoutonReset["bg"]="black"
        self.BoutonReset["fg"]="white"
        self.BoutonReset.place(x=70,y=572)

    def FonctionRetour(self):
        self.pack_forget()
        self.interface1.pack()

    def FonctionRetourNiveau1(self):
        self.pack_forget()
        self.interface2.pack()

    def FonctionRetourNiveau2(self):
        self.pack_forget()
        self.interface3.pack()

    def FonctionRetourNiveau3(self):
        self.pack_forget()
        self.interface4.pack()

    def FonctionRetourNiveau4(self):
        self.pack_forget()
        self.interface5.pack()

    def Lancer(self,nb,mode=1,nbNiveau=""):
        self.pack_forget()
        music.fadeout(100)
        music.load("Core/Son/427452__sirkoto51__atmospheric-ambiance-loop-3.wav")
        music.set_volume(0.2)
        music.play(-1)
        niveau=ModulePrincipale.Niveau(self.fenetre,nb,self,mode)

    def Suite(self,result,nbNiveau=""):
        if result == 1:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            self.pack()
        elif result == 0:
            self.fenetre.destroy()
        elif result == 2:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            with open("Core/Save/{}".format(self.interface6.save), 'rb') as fichier: #Utilisation du module pickle
                depickler = pickle.Unpickler(fichier)
                nbDebloque = depickler.load() #Chargement du fichier

            if int(nbDebloque)==int(nbNiveau):
                if int(nbNiveau) <10:
                    nbDebloque = "0"+str(int(nbNiveau)+1)
                elif int(nbNiveau) <20:
                    nbDebloque = str(int(nbNiveau)+1)
                else:
                    nbDebloque=nbNiveau

                with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                    pickler = pickle.Pickler(fichier)
                    pickler.dump(nbDebloque) #Enregistrement

            self.interface6.FonctionLancerSave(self.interface6.save)
            self.pack()

    def Reinitialiser(self):
        if askyesno("Reinitialiser ?","Voulez-vous reinitialiser la sauvegarde ? \n(Cette action est irreversible)"):
            if self.interface6.save == "1":
                nbDebloque="20"
            else:
                nbDebloque="01"
            with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                pickler = pickle.Pickler(fichier)
                pickler.dump(nbDebloque) #Enregistrement
            showinfo("Reinitialisation","Reinitialisation reussi !")
            self.interface6.FonctionLancerSave(self.interface6.save)


class InterfaceNiveau4(Frame):
    def __init__(self,fenetre,bliblison):
        self.fenetre=fenetre
        self.bliblison=bliblison
        Frame.__init__(self,self.fenetre, width=1000, height=650)
        self.pack_propagate(0)
        self.canvas = Canvas(self, bg='black', width=1000, height=650)
        self.canvas.pack()

        self.interface1=Frame
        self.interface2=Frame
        self.interface3=Frame
        self.interface4=Frame
        self.interface5=Frame
        self.interface6=Frame

        self.fond= PhotoImage(file=chemin+'fondniveaub.gif')   #image de fond
        self.canvas.create_image(500,325, image=self.fond)

        self.BoutonQuitter = Button(self, text="Quitter",command=self.fenetre.destroy) #Bouton quitte
        self.BoutonQuitter["bg"]="black"
        self.BoutonQuitter["fg"]="white"
        self.BoutonQuitter.place(x=10,y=600)

        self.ImageBouton5= PhotoImage(file=chemin+'BoutonRetour.gif')           #Bouton retour
        self.BoutonRetour = Button(self, image=self.ImageBouton5,width=90, height=40,borderwidth=0,highlightthickness=0, command=self.FonctionRetour)
        self.BoutonRetour["bg"]="black"
        self.BoutonRetour["fg"]="white"
        self.BoutonRetour.place(x=900,y=580)

        self.ImageNiveau16= PhotoImage(file=chemin+'niveau16.gif')           #Bouton Niveau 16
        self.BoutonNiveau16 = Button(self, image=self.ImageNiveau16,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("16"))
        self.BoutonNiveau16["bg"]="black"
        self.BoutonNiveau16["fg"]="white"
        self.BoutonNiveau16.place(x=247,y=406)

        self.ImageNiveau17= PhotoImage(file=chemin+'niveau17.gif')           #Bouton Niveau 17
        self.BoutonNiveau17 = Button(self, image=self.ImageNiveau17,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("17"))
        self.BoutonNiveau17["bg"]="black"
        self.BoutonNiveau17["fg"]="white"
        self.BoutonNiveau17.place(x=665,y=448)

        self.ImageNiveau18= PhotoImage(file=chemin+'niveau18.gif')           #Bouton Niveau 18
        self.BoutonNiveau18 = Button(self, image=self.ImageNiveau18,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("18"))
        self.BoutonNiveau18["bg"]="black"
        self.BoutonNiveau18["fg"]="white"
        self.BoutonNiveau18.place(x=485,y=302)

        self.ImageNiveau19= PhotoImage(file=chemin+'niveau19.gif')           #Bouton Niveau 19
        self.BoutonNiveau19 = Button(self, image=self.ImageNiveau19,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("19"))
        self.BoutonNiveau19["bg"]="black"
        self.BoutonNiveau19["fg"]="white"
        self.BoutonNiveau19.place(x=279,y=100)

        self.ImageNiveau20= PhotoImage(file=chemin+'niveau20.gif')           #Bouton Niveau 20
        self.BoutonNiveau20 = Button(self, image=self.ImageNiveau20,width=180, height=80,borderwidth=0,highlightthickness=0, command=lambda:self.Lancer("20"))
        self.BoutonNiveau20["bg"]="black"
        self.BoutonNiveau20["fg"]="white"
        self.BoutonNiveau20.place(x=640,y=133)

        self.ImageRetour1= PhotoImage(file=chemin+'retour1.gif')           #Bouton Retour Niveau 1
        self.BoutonRetour1 = Button(self, image=self.ImageRetour1,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau1 )
        self.BoutonRetour1["bg"]="black"
        self.BoutonRetour1["fg"]="white"
        self.BoutonRetour1.place(x=318,y=572)

        self.ImageRetour2= PhotoImage(file=chemin+'retour2.gif')           #Bouton Retour Niveau 2
        self.BoutonRetour2 = Button(self, image=self.ImageRetour2,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau2 )
        self.BoutonRetour2["bg"]="black"
        self.BoutonRetour2["fg"]="white"
        self.BoutonRetour2.place(x=415,y=572)

        self.ImageRetour3= PhotoImage(file=chemin+'retour3.gif')           #Bouton Retour Niveau 3
        self.BoutonRetour3 = Button(self, image=self.ImageRetour3,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau3 )
        self.BoutonRetour3["bg"]="black"
        self.BoutonRetour3["fg"]="white"
        self.BoutonRetour3.place(x=515,y=572)

        self.ImageRetour4= PhotoImage(file=chemin+'retour4.gif')           #Bouton Retour Niveau 4
        self.BoutonRetour4 = Button(self, image=self.ImageRetour4,width=50, height=50,borderwidth=0,highlightthickness=0, command=self.FonctionRetourNiveau4)
        self.BoutonRetour4["bg"]="black"
        self.BoutonRetour4["fg"]="white"
        self.BoutonRetour4.place(x=615,y=572)

        self.ImageReset= PhotoImage(file=chemin+'reset.gif')
        self.BoutonReset= Button(self, image=self.ImageReset, width=50, height=50,borderwidth=0,highlightthickness=0, command=self.Reinitialiser)
        self.BoutonReset["bg"]="black"
        self.BoutonReset["fg"]="white"
        self.BoutonReset.place(x=70,y=572)

    def FonctionRetour(self):
        self.pack_forget()
        self.interface1.pack()

    def FonctionRetourNiveau1(self):
        self.pack_forget()
        self.interface2.pack()

    def FonctionRetourNiveau2(self):
        self.pack_forget()
        self.interface3.pack()

    def FonctionRetourNiveau3(self):
        self.pack_forget()
        self.interface4.pack()

    def FonctionRetourNiveau4(self):
        self.pack_forget()
        self.interface5.pack()

    def Lancer(self,nb,mode=1):
        self.pack_forget()
        music.fadeout(100)
        music.load("Core/Son/427452__sirkoto51__atmospheric-ambiance-loop-3.wav")
        music.set_volume(0.2)
        music.play(-1)
        niveau=ModulePrincipale.Niveau(self.fenetre,nb,self,mode)

    def Suite(self,result,nbNiveau=""):
        if result == 1:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            self.pack()
        elif result == 0:
            self.fenetre.destroy()
        elif result == 2:
            music.fadeout(100)
            music.load("Core/Son/397089__timbre__remix-of-erokia-s-freesound-394011.wav")
            music.set_volume(0.5)
            music.play(-1)
            with open("Core/Save/{}".format(self.interface6.save), 'rb') as fichier: #Utilisation du module pickle
                depickler = pickle.Unpickler(fichier)
                nbDebloque = depickler.load() #Chargement du fichier

            if int(nbDebloque)==int(nbNiveau):
                if int(nbNiveau) <10:
                    nbDebloque = "0"+str(int(nbNiveau)+1)
                elif int(nbNiveau) <20:
                    nbDebloque = str(int(nbNiveau)+1)
                else:
                    nbDebloque=nbNiveau

                with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                    pickler = pickle.Pickler(fichier)
                    pickler.dump(nbDebloque) #Enregistrement

            self.interface6.FonctionLancerSave(self.interface6.save)
            self.pack()

    def Reinitialiser(self):
        if askyesno("Reinitialiser ?","Voulez-vous reinitialiser la sauvegarde ? \n(Cette action est irreversible)"):
            if self.interface6.save == "1":
                nbDebloque="20"
            else:
                nbDebloque="01"
            with open("Core/Save/{}".format(self.interface6.save), 'wb') as fichier: #Utilisation du module pickle
                pickler = pickle.Pickler(fichier)
                pickler.dump(nbDebloque) #Enregistrement
            showinfo("Reinitialisation","Reinitialisation reussi !")
            self.interface6.FonctionLancerSave(self.interface6.save)
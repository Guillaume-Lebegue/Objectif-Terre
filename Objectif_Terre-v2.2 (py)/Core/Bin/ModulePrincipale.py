#-------------------------------------------------------------------------------
# Name:        ModulePrincipale
# Purpose:     Module de fonction/class concernant le logiciel Objectif_Terre
#
# Author:      Guillaume Lebegue
#
# Copyright:   (c) ikkino 2018
#-------------------------------------------------------------------------------

##Importation des modules necessaires
from tkinter import *
from tkinter.messagebox import *
from PIL import ImageTk
from PIL import Image
import Core.Bin.ModuleCarte
from random import randint

##Class-------------------------------------------------------------------------
class Niveau(Canvas): #Herite de Frame
    """Class chargant un niveau du jeu
    cree des rangee de frame
    contenat des cases(canavas)
    place l'icone du joueur
    et des boutons de jeu
    demande une fenetre parent, le numero de la map
    possede:
        -Une fenetre parent
        -Un numero de map
        -Une liste de rangee(frame)
        -Coordone d'un point de depart
        -Une carte
        -Des ressources
        -Un perso(objet)
        -Des boutons de controles
    a pour fonction:
        -Genere
        -Supprime
        -Actualise
        -GenereRangee
        -GenereCase
        -Avancer
        -Tourner a Gauche
        -Tourner a Droite
    """
    def __init__(self,fenetre,numeroMap,interfacePar,mode=1,personnal=0,**kwargs):
        """Constructeurde la class niveau
        demande une fenetre parent et le numero de la carte
        """
    ##Initialisation------------------------------------------------------------
        ##Variable---------------------
        self.fenetre=fenetre #Fenetre parent
        self.numeroMap=numeroMap #Numero de la carte
        self.listeRangee=[] #Liste de rangee(frame)
        self.startR=0 #Coordonee point depart y
        self.startC=0 #Coordonee point depart x
        self.listeAct=[]
        self.listeActPrec=[]
        self.listeActSuiv=[]
        self.listeBoite=[]
        self.stop = IntVar()
        self.fin = False
        self.quitter = False
        self.interfacePar=interfacePar
        self.mode=mode
        self.personnal=personnal

        Canvas.__init__(self, self.fenetre, width=1000, height=650,**kwargs) #Constructeur frame

        ##Ressources Cores----------------------------------------------------------
        self.imgTFlecheAS = Image.open("Core/Ressources/Core/Fleche_Avancer.gif")
        self.imgTFlecheA = ImageTk.PhotoImage(self.imgTFlecheAS,master=self) #Charge l'image
        self.imgTFlecheAG = ImageTk.PhotoImage(self.imgTFlecheAS.rotate(90),master=self)
        self.imgTFlecheAD = ImageTk.PhotoImage(self.imgTFlecheAS.rotate(270),master=self)

        self.pack()
        self.pack_propagate(0)

        self.imgFond = PhotoImage(file="Core/Ressources/Interface/fond jeux.gif",master=self)
        self.create_image(500,325,image=self.imgFond)

        self.imgJouer= ImageTk.PhotoImage(file="Core/Ressources/Core/Play.gif")
        self.imgTFlecheTD = ImageTk.PhotoImage(file="Core/Ressources/Core/Fleche_Touner_Droit.gif",master=self) #Charge l'image
        self.imgTFlecheTG = ImageTk.PhotoImage(file="Core/Ressources/Core/Fleche_Touner_Gauche.gif",master=self) #Charge l'image
        self.imgTFlecheS = ImageTk.PhotoImage(file="Core/Ressources/Core/Flech_Sauter.gif",master=self) #Charge l'image
        self.imgTakeDrop = ImageTk.PhotoImage(file="Core/Ressources/Core/Fleche_Prendre.gif",master=self)

        self.imgGFlecheA = ImageTk.PhotoImage(file="Core/Ressources/Core/Fleche_Avancer_100X100.gif",master=self)
        self.imgGFlecheTD = ImageTk.PhotoImage(file="Core/Ressources/Core/Fleche_Tourner_Droit_100X100.gif",master=self)
        self.imgGFlecheTG = ImageTk.PhotoImage(file="Core/Ressources/Core/Fleche_Tourner_Gauche_100X100.gif",master=self)
        self.imgGTakeDrop= ImageTk.PhotoImage(file="Core/Ressources/Core/Fleche_Prendre_100x100.gif",master=self)
        self.imgQuit = ImageTk.PhotoImage(file="Core/Ressources/Core/Sorti.gif",master=self)
        self.imgAide = ImageTk.PhotoImage(file="Core/Ressources/Core/Bouton_Aide.gif",master=self)

        self.manuel=InterfaceManuelDutilisation(self.fenetre,self.interfacePar.bliblison)
        self.manuel.interfaceAcceuil=self

        ##Frame------------------------
            ##Frame gauche
        self.squeFrameG=Canvas(self,highlightthickness=0)
        self.squeFrameG.pack(side=LEFT,fill=Y)
        self.squeFrameG.create_image(500,325,image=self.imgFond)

        self.frameG=Canvas(self.squeFrameG,borderwidth=0,width=200,height=520,bg='red',highlightthickness=0)
        self.frameG.pack(side=TOP)
        self.frameG.pack_propagate(0)
        self.frameG.create_image(500,325,image=self.imgFond)

        self.boutonActG=Button(self.frameG,image=self.imgTFlecheAG,state='disabled',command=self.ActionDepG)
        self.boutonActG.pack(side=LEFT)

        self.frameGSep=Canvas(self.frameG,borderwidth=0,width=10,height=50,highlightthickness=0)
        self.frameGSep.pack(side=LEFT)
        self.frameGSep.pack_propagate(0)
        self.frameGSep.create_image(500,100,image=self.imgFond)

        self.frameGG=Frame(self.frameG,borderwidth=0,width=52,height=520)
        self.frameGG.pack(side=LEFT)
        self.frameGG.pack_propagate(0)

        self.frameSepG=Canvas(self.frameG,borderwidth=0,width=10,height=50,highlightthickness=0)
        self.frameSepG.pack(side=LEFT)
        self.frameSepG.pack_propagate(0)
        self.frameSepG.create_image(500,100,image=self.imgFond)

        self.frameGD=Frame(self.frameG,borderwidth=0,width=52,height=520)
        self.frameGD.pack(side=LEFT)
        self.frameGD.pack_propagate(0)

        self.frameBoutonMG=Canvas(self.squeFrameG,borderwidth=0,highlightthickness=0)
        self.frameBoutonMG.pack(side=BOTTOM)
        self.frameBoutonMG.create_image(466,-195,image=self.imgFond)

        self.boutonQuit=Button(self.frameBoutonMG,image=self.imgQuit,command=self.Retour)
        self.boutonQuit.pack(side=LEFT)

        self.frameBoutonSep=Canvas(self.frameBoutonMG,width=20,borderwidth=0,highlightthickness=0)
        self.frameBoutonSep.pack(side=LEFT)
        self.frameBoutonSep.create_image(410,-195,image=self.imgFond)

        self.boutonAide=Button(self.frameBoutonMG,image=self.imgAide,command=self.Aide)
        self.boutonAide.pack(side=RIGHT)

            ##Frame droite
        self.squeFrameD=Canvas(self,borderwidth=0,highlightthickness=0)
        self.squeFrameD.pack(side=RIGHT,fill=Y)
        self.squeFrameD.create_image(-305,325,image=self.imgFond)

        self.frameD=Canvas(self.squeFrameD,borderwidth=0,width=200,height=520,highlightthickness=0)
        self.frameD.pack(side=TOP)
        self.frameD.pack_propagate(0)
        self.frameD.create_image(-305,325,image=self.imgFond)

        self.boutonActD=Button(self.frameD,image=self.imgTFlecheAD,state='disabled',command=self.ActionDepD)
        self.boutonActD.pack(side=RIGHT)

        self.frameDSep=Canvas(self.frameD,borderwidth=0,width=10,height=50,highlightthickness=0)
        self.frameDSep.pack(side=RIGHT)
        self.frameDSep.pack_propagate(0)
        self.frameDSep.create_image(500,100,image=self.imgFond)

        self.frameDD=Frame(self.frameD,borderwidth=0,width=52,height=520)
        self.frameDD.pack(side=RIGHT)
        self.frameDD.pack_propagate(0)

        self.frameSepD=Canvas(self.frameD,borderwidth=0,width=10,height=50,highlightthickness=0)
        self.frameSepD.pack(side=RIGHT)
        self.frameSepD.pack_propagate(0)
        self.frameSepD.create_image(500,100,image=self.imgFond)

        self.frameDG=Frame(self.frameD,borderwidth=0,width=52,height=520)
        self.frameDG.pack(side=RIGHT)
        self.frameDG.pack_propagate(0)

        self.boutonStart=Button(self.squeFrameD,image=self.imgJouer,state='disabled',command=self.Start)
        self.boutonStart.pack(side=BOTTOM)

            ##Frame centre
        self.frameC=Canvas(self,height=650,borderwidth=0,width=600,highlightthickness=0)
        self.frameC.pack(fill=BOTH)
        self.frameC.pack_propagate(0)
        self.frameC.create_image(300,325,image=self.imgFond)

        self.labelNiveau=Label(self.frameC, text="Niveau: {}".format(self.numeroMap))
        self.labelNiveau.pack(side=TOP)

    ##Chargement carte----------------------------------------------------------
        if self.personnal == 0:
            self.carte=Core.Bin.ModuleCarte.Ouvrir(self.numeroMap) #Ouvre la carte
        elif self.personnal == 1:
            self.carte=Core.Bin.ModuleCarte.Ouvrir(self.numeroMap,1) #Ouvre la carte
        self.carte.ressources=Core.Bin.ModuleCarte.Ressources(self.carte.biome) #Charge les ressources

        self.nbAvencer=self.carte.nbAvancer
        self.nbTournerG=self.carte.nbTournerG
        self.nbTournerD=self.carte.nbTournerD
        self.nbTakeDrop=self.carte.nbTakeDrop

        ##Trouve la case de depart----------------------------------------------
        nbRangee=0
        for rangee in self.carte.listerangee: #Pour chaques rangees de la liste
            nbCase=0
            for case in rangee.listecase: #Pour chaques cases dans la rangee
                if case.img == 10: #Si la case est la case de depart
                    self.startR=nbRangee #Charge coordonee y
                    self.startC=nbCase #Charge coordonee x
                nbCase+=1
            nbRangee+=1

        ##Cree les cases
        u=0
        for i in self.carte.listerangee: #Pour chaque rangee de la carte
            self.GenereRangee() #Cree une rangee
            for e in i.listecase: #Pour chaque case de la rangee
                self.GenereCase(self.listeRangee[u], e) #Cree une case dans la rangee
            u+=1

        ##Lie les cases
        for rangee in self.listeRangee: #Pour chaques rangee
            for case in rangee.listeCase: #Pour chaques cases de la rangee
                if case.case.liaison!='': #Si il y a une liaison
                    for rangee2 in self.listeRangee: #Pour chaques rangee
                        for case2 in rangee2.listeCase: #Pour chaques cases de la rangee
                            if case.case.liaison==case2.case: #Si il s'aggit de la bonne liaison
                                case.liaison=case2

        ##Charge perso----------------------------------------------------------
        self.perso=Perso(self, self.startR, self.startC, self.carte.oriPers) #Cree un nouveau perso

        ##Charge Boite
        y=0
        for rangee in self.carte.listerangee:
            x=0
            for case in rangee.listecase:
                if case.img==5:
                    boite=Boite(self,y,x)
                    self.listeBoite.append(boite)
                x+=1
            y+=1

        ##Genere la position du perso et des boites-----------------------------
        self.GenereP() #Fonction de la class
        self.GenereB()

    ##Boutons-------------------------------------------------------------------
        self.frameBouton = Frame(self.frameC)
        self.frameBouton.pack(side=BOTTOM)

        self.frameBoutonAv = Frame(self.frameBouton)
        self.frameBoutonAv.pack(fill=Y,side=LEFT)
        self.varnbAvancer=StringVar(self,self.nbAvencer)
        self.nbBoutAv= Label(self.frameBoutonAv, textvariable=self.varnbAvancer)
        self.nbBoutAv.pack(side=TOP)
        self.boutonAv = Button(self.frameBoutonAv, height=100, width= 100, image=self.imgGFlecheA ,command=self.Avancer)
        self.boutonAv.pack(side=BOTTOM)

        self.frameBoutonTG = Frame(self.frameBouton)
        self.frameBoutonTG.pack(fill=Y,side=LEFT)
        self.varnbTournerG=StringVar(self,self.nbTournerG)
        self.nbBoutTG= Label(self.frameBoutonTG, textvariable=self.varnbTournerG)
        self.nbBoutTG.pack(side=TOP)
        self.boutonTG = Button(self.frameBoutonTG, height=100, width= 100,image=self.imgGFlecheTG, command=self.TournerG)
        self.boutonTG.pack(side=BOTTOM)

        self.frameBoutonTD = Frame(self.frameBouton)
        self.frameBoutonTD.pack(fill=Y,side=LEFT)
        self.varnbTournerD=StringVar(self,self.nbTournerD)
        self.nbBoutTD= Label(self.frameBoutonTD, textvariable=self.varnbTournerD)
        self.nbBoutTD.pack(side=TOP)
        self.boutonTD = Button(self.frameBoutonTD, height=100, width= 100,image=self.imgGFlecheTD, command=self.TournerD)
        self.boutonTD.pack(side=BOTTOM)

        self.frameBouton4 = Frame(self.frameBouton)
        self.frameBouton4.pack(fill=Y,side=LEFT)
        self.varnbTakeDrop=StringVar(self,self.nbTakeDrop)
        self.nbBout4= Label(self.frameBouton4, textvariable=self.varnbTakeDrop)
        self.nbBout4.pack(side=TOP)
        self.bouton4 = Button(self.frameBouton4, height=100, width= 100,image=self.imgGTakeDrop, command=self.ActTackDrop)
        self.bouton4.pack(side=BOTTOM)

    ##Frame de l'histoire-------------------------------------------------------
        self.frameHistoire=Frame(self.frameC,bg='white', width=425, height=125)
        self.frameHistoire.pack_propagate(0)
        self.frameHistoire.bind("<Button-1>",self.next_dialog) #Appele self.Clic si on clic sur la frame
        self.fenetre.protocol("WM_DELETE_WINDOW", self.Quitter)
        self.frameLabelClic=Frame(self.frameHistoire,bg='white')
        self.frameLabelClic.pack(side=BOTTOM,fill=X)
        self.frameLabelClic.bind("<Button-1>",self.next_dialog) #Appele self.Clic si on clic sur la frame
        self.labelClic=Label(self.frameLabelClic,bg='white',text="Clic !")
        self.labelClic.pack(side=RIGHT)
        self.labelClic.bind("<Button-1>",self.next_dialog) #Appele self.Clic si on clic sur le label

        self.ActuNBAct()

        self.Histoire(0)

    def Aide(self):
        self.pack_forget()
        self.manuel.pack()

    def Quitter(self):
        if askyesno("Quitter ?", "Voulez vous quitter ? \nLa progression ne seras pas sauvegarder"):
            if self.fin:
                self.stop.set(1)
                self.quitter = True

            else:
                self.interfacePar.Suite(0)

    def Fin(self):
        """Methode de la class Niveau
        Lance l'histoire de fin
        puis detruit le niveau, permettant la poursuite du programe
        """
        self.fin = True
        if self.carte.histSuiv != []:
            self.Histoire(1)
            self.fenetre.wait_variable(self.stop)

        if self.quitter:
            self.interfacePar.Suite(0)

        else:
            self.fenetre.protocol("WM_DELETE_WINDOW", self.fenetre.destroy)
            self.interfacePar.Suite(2,self.numeroMap)
            self.destroy()

    def Retour(self):
        if askyesno("Quitter ?", "Voulez vous quitter ?"):
            self.fenetre.protocol("WM_DELETE_WINDOW", self.fenetre.destroy)
            self.interfacePar.Suite(1)
            self.destroy()

    def Histoire(self,startend):
        """Methode de la class Niveau
        Retire la frame des boutons et affiche celle de l'histoire
        puis affiche l'hitoire en attandant un clic de l'utilisateur
        pour afficher la suite
        a la fin, retire la frame histoire et affiche celle des boutons
        demande si c'est le debut(0) ou la fin(1)
        """
        if startend==0:
            histAFaire = self.carte.histPrec#Recupere l'histoire voulue

        elif startend==1:
            histAFaire = self.carte.histSuiv

        if histAFaire != []:
            self.hist_iter = iter(histAFaire)

            self.frameBouton.pack_forget() #Retire la fgrme des boutons

            self.frameHistoire.pack(side=BOTTOM) #Affiche la frame de l'histoire

            #Pour chaques dialogues de l'histoire
            self.frameLabel=Frame(self.frameHistoire,bg='white')
            self.frameLabel.pack(fill=Y)
            self.frameLabel.bind("<Button-1>",self.next_dialog) #Appele self.Clic si on clic sur la frame

            #Pour chaques lignes du dialogue
            histASuiv=next(self.hist_iter)
            for ligne in histASuiv:
                label=Label(self.frameLabel,text=ligne,bg='white')
                label.pack(side=TOP)
                label.bind("<Button-1>",self.next_dialog) #Appele self.Clic si on clic sur le label

            self.fenetre.update() #Met a jour la fenetre

    def next_dialog(self, event=None):
        try:
            histASuiv=next(self.hist_iter)
            self.frameLabel.destroy()

            self.frameLabel=Frame(self.frameHistoire,bg='white')
            self.frameLabel.pack(fill=Y)
            self.frameLabel.bind("<Button-1>",self.next_dialog) #Appele self.Clic si on clic sur la frame

            for ligne in histASuiv:
                label=Label(self.frameLabel,text=ligne,bg='white')
                label.pack(side=TOP)
                label.bind("<Button-1>",self.next_dialog) #Appele self.Clic si on clic sur le label

        except StopIteration:
            del self.hist_iter
            self.frameLabel.destroy() #Detruit le dialogue
            self.frameHistoire.pack_forget() #Retire la frame d'histoire
            self.frameBouton.pack(side=BOTTOM) #Affiche la frame des boutons
            self.stop.set(1)

    def ActuNBAct(self):
        """Methode de la class Niveau
        Actualise le nombre d'action
        ainsi que les label les affichants
        """
        nbAvencer=int(self.varnbAvancer.get())
        nbTournerG=int(self.varnbTournerG.get())
        nbTournerD=int(self.varnbTournerD.get())
        nbTakeDrop=int(self.varnbTakeDrop.get())

        #Si =-1 alors, infini de l'action et suppression du label
        if nbAvencer == -1:
            self.boutonAv.config(state='normal')
            self.nbBoutAv.pack_forget()

        #Si =0 alors, grisement du boutons
        elif nbAvencer == 0:
            self.boutonAv.config(state=DISABLED)
            self.nbBoutAv.pack(side=TOP)

        #Sinon Bouton normal
        else:
            self.boutonAv.config(state='normal')
            self.nbBoutAv.pack(side=TOP)

        if nbTournerG == -1:
            self.boutonTG.config(state='normal')
            self.nbBoutTG.pack_forget()

        elif nbTournerG == 0:
            self.boutonTG.config(state=DISABLED)
            self.nbBoutTG.pack(side=TOP)

        else:
            self.boutonTG.config(state='normal')
            self.nbBoutTG.pack(side=TOP)

        if nbTournerD == -1:
            self.boutonTD.config(state='normal')
            self.nbBoutTD.pack_forget()

        elif nbTournerD == 0:
            self.boutonTD.config(state=DISABLED)
            self.nbBoutTD.pack(side=TOP)

        else:
            self.boutonTD.config(state='normal')
            self.nbBoutTD.pack(side=TOP)

        if nbTakeDrop == -1:
            self.bouton4.config(state='normal')
            self.nbBout4.pack_forget()

        elif nbTakeDrop == 0:
            self.bouton4.config(state=DISABLED)
            self.nbBout4.pack(side=TOP)

        else:
            self.bouton4.config(state='normal')
            self.nbBout4.pack(side=TOP)

    def Reinitialise(self):
        """Methode de la class niveau
        reinitialise les cases modifiable
        les pos de perso et de boite
        puis actualise
        """
        for rangee in self.listeRangee: #Pour chaques rangee
            for case in rangee.listeCase: #Pour chaque case de la rangee
                if case.case.img==1.2: #Si la case est un pont modifier
                    case.case.img=1
                    case.delete('PontON')
                    case.create_image(25, 25, image=self.carte.ressources.imgPontFN, tag='PontFN')

                elif case.case.img==2.2: #Si la case est un pont modifier
                    case.case.img=2
                    case.delete('PontOO')
                    case.create_image(25, 25, image=self.carte.ressources.imgPontFO, tag='PontFO')

                elif case.case.img==3.2: #Si la case est un bouton modifier
                    case.case.img=3
                    case.delete('BoutonJF')
                    case.create_image(25, 25, image=self.carte.ressources.imgBoutonJO, tag='BoutonJO')

        self.perso.posH=self.startR #Reinitialise pos h du perso
        self.perso.posL=self.startC #Reinitialise pos l du perso
        self.listeBoite=[] #Reinitialise les boites
        self.perso.porte=""

        #Regenere les boites
        y=0
        for rangee in self.carte.listerangee:
            x=0
            for case in rangee.listecase:
                if case.img==5:
                    boite=Boite(self,y,x)
                    self.listeBoite.append(boite)
                x+=1
            y+=1

        self.perso.orien=self.carte.oriPers #Regenere l'orientation du perso

        self.varnbAvancer.set(self.nbAvencer)
        self.varnbTakeDrop.set(self.nbTakeDrop)
        self.varnbTournerD.set(self.nbTournerD)
        self.varnbTournerG.set(self.nbTournerG)

        self.Actualise()

    def GenereP(self):
        """Fonction de la class niveau
        Cree des rangees(frames)
        des cases(canvas)
        en fonctions des differentes listes
        place le perso sur la map en fonction
        de sa position et de son orientation
        """
        #orientation du personage
        if self.perso.orien == 'N':
            self.listeRangee[self.perso.posH].listeCase[self.perso.posL].create_image(25, 25, image=self.carte.ressources.imgPersoN, tag='Perso')

        elif self.perso.orien == 'S':
            self.listeRangee[self.perso.posH].listeCase[self.perso.posL].create_image(25, 25, image=self.carte.ressources.imgPersoS, tag='Perso')

        elif self.perso.orien == 'O':
            self.listeRangee[self.perso.posH].listeCase[self.perso.posL].create_image(25, 25, image=self.carte.ressources.imgPersoO, tag='Perso')

        elif self.perso.orien == 'E':
            self.listeRangee[self.perso.posH].listeCase[self.perso.posL].create_image(25, 25, image=self.carte.ressources.imgPersoE, tag='Perso')

    def GenereB(self):
        """Fonction de la class niveau
        Affiche les images de toutes les boites
        """
        for boite in self.listeBoite:
            self.listeRangee[boite.posH].listeCase[boite.posL].create_image(25, 25, image=self.carte.ressources.imgBoite, tag='Boite')

    def SupprimeP(self):
        """Fonction de la class niveau
        Supprime le perso
        """
        for rangee in self.listeRangee:
            for case in rangee.listeCase:
                case.delete('Perso')

    def SupprimeB(self):
        """Methode de la class niveau
        Supprime les images de boite
        """
        for rangee in self.listeRangee:
            for case in rangee.listeCase:
                case.delete('Boite')

    def Actualise(self):
        """Fonction de la class niveau
        Appele les fonctions permettant d'actualiser
        """
        self.SupprimeP()
        self.GenereP()
        self.SupprimeB()
        self.GenereB()

    def GenereRangee(self):
        """Fonction de l'interface
        creant des rangee de la carte
        """
        rangee=Rangee(self.frameC)
        self.listeRangee.append(rangee) #Ajout a la liste de rangee

    def GenereCase(self, rangee, case):
        """Fonction de la class niveau
        creant des cases de la carte
        demande une rangee parent
        et une case de la carte
        """
        case=Case(self, rangee, case) #Cree objet case
        rangee.listeCase.append(case) #Ajoute la case a la liste de la rangee

    def Avancer(self):
        """Fonction de la class niveau
        Cree une action
        et retire de 1 le nombre d'action restante
        """
        action=Action(self, 'Avancer')

        intTemp = int(self.varnbAvancer.get())
        if intTemp>0:
            intTemp-=1
            self.varnbAvancer.set(intTemp)
            self.ActuNBAct()

    def TournerG(self):
        """Fonction de la class niveau
        Cree une action
        et retire de 1 le nombre d'action restante
        """
        action=Action(self, 'TournerG')

        intTemp = int(self.varnbTournerG.get())
        if intTemp>0:
            intTemp-=1
            self.varnbTournerG.set(intTemp)
            self.ActuNBAct()

    def TournerD(self):
        """Fonction de la class niveau
        Cree une action
        et retire de 1 le nombre d'action restante
        """
        action=Action(self, 'TournerD')

        intTemp = int(self.varnbTournerD.get())
        if intTemp>0:
            intTemp-=1
            self.varnbTournerD.set(intTemp)
            self.ActuNBAct()

    def ActTackDrop(self):
        """Fonction de la class niveau
        Cree une action
        et retire de 1 le nombre d'action restante
        """
        action=Action(self, 'TakeDrop')

        intTemp = int(self.varnbTakeDrop.get())
        if intTemp>0:
            intTemp-=1
            self.varnbTakeDrop.set(intTemp)
            self.ActuNBAct()

    def TakeDrop(self):
        """Fonction de la class niveau
        Si le perso ne porte pas de boite:
            Regarde si devant lui il y en a une
            si oui, la prend
        Si il porte une boite:
            Regarde si devant lui il peut poser une boit
            Si oui, la pose
        """
        if self.perso.porte!='': #Si le perso porte quelque chose
            #Recupere la case suivante
            if self.perso.orien=='N':
                caseSuiv=(self.perso.posH-1,self.perso.posL)

            elif self.perso.orien=='E':
                caseSuiv=(self.perso.posH,self.perso.posL+1)

            elif self.perso.orien=='S':
                caseSuiv=(self.perso.posH+1,self.perso.posL)

            elif self.perso.orien=='O':
                caseSuiv=(self.perso.posH,self.perso.posL-1)

            intrus=False
            #Boite sur la case ?
            for boite in self.listeBoite:
                posBoite=(boite.posH,boite.posL)
                if posBoite==caseSuiv:
                    intrus=True

            if not intrus: #Si sans intru
                caseSuivY,caseSuivX=caseSuiv
                caseSuiv=self.listeRangee[caseSuivY].listeCase[caseSuivX].case.img
                if caseSuiv==5 or caseSuiv==4: #Si la case est une case a boite ou un bouton
                    self.perso.porte.posH=caseSuivY #Change la posH de la boite
                    self.perso.porte.posL=caseSuivX #Change la posL de la boite
                    self.perso.porte='' #Pose la boite

                    if self.listeRangee[caseSuivY].listeCase[caseSuivX].case.img==4: #Si un bouton a boite
                        self.listeRangee[caseSuivY].listeCase[caseSuivX].liaison.Actione() #Active l'action

                    self.Actualise() #Actualise

        elif self.perso.porte=='': #Si ne porte pas
            if self.perso.orien=='N':
                caseSuiv=(self.perso.posH-1,self.perso.posL)

            elif self.perso.orien=='E':
                caseSuiv=(self.perso.posH,self.perso.posL+1)

            elif self.perso.orien=='S':
                caseSuiv=(self.perso.posH+1,self.perso.posL)

            elif self.perso.orien=='O':
                caseSuiv=(self.perso.posH,self.perso.posL-1)

            for boite in self.listeBoite:
                posBoite=(boite.posH,boite.posL)
                if caseSuiv==posBoite: #Si il y a une boite sur la case en face
                    boite.posH=self.perso.posH
                    boite.posL=self.perso.posL
                    self.perso.porte=boite #Recupere la boite

                    posSuivY,posSuivX=caseSuiv
                    if self.listeRangee[posSuivY].listeCase[posSuivX].case.img==4: #Si la case ou on prend la boite est un bouton a boite
                        self.listeRangee[posSuivY].listeCase[posSuivX].liaison.Actione() #Active

                    self.Actualise() #Actualise

    def AddAction(self, action):
        """Fonction de la class niveau
        Demande une action(class) qu'il ajoute
        a la liste d'action
        si la liste d'action est pleine,
        repartit sur les autres listes
        puis appelle la fonction ActuAction
        """
        if len(self.listeAct)<=39:
            self.listeAct.append(action)
        else:
            self.listeActSuiv.append(action)
        self.ActuAction()

    def ActuAction(self):
        """Fonction de la class niveau
        actualise les colones d'action
        """
        self.listeAct[0].bouton.config(bg='white')
        for action in self.listeAct:
            action.bouton.pack_forget()

        if len(self.listeActSuiv)>0:
            self.boutonActD.config(state='normal')

        else:
            self.boutonActD.config(state='disabled')

        if len(self.listeActPrec)>0:
            self.boutonActG.config(state='normal')

        else:
            self.boutonActG.config(state='disabled')

        if len(self.listeActPrec)==0:
            self.listeAct[0].bouton.config(bg='red')

        if len(self.listeAct)>0:
            self.boutonStart.config(state='normal')

        nbAction=len(self.listeAct)
        i=0
        while nbAction>i:
            if i<10:
                self.listeAct[i].bouton.pack(side=TOP, in_=self.frameGG)

            elif i<20:
                self.listeAct[i].bouton.pack(side=TOP, in_=self.frameGD)

            elif i<30:
                self.listeAct[i].bouton.pack(side=TOP, in_=self.frameDG)

            elif i<40:
                self.listeAct[i].bouton.pack(side=TOP, in_=self.frameDD)
            i+=1

    def ActionDepD(self):
        """Methode  de la class niveau
        Deplace les action vers la droite
        """
        self.listeAct[0].bouton.config(bg='white')
        for i in range(0,10):
            self.listeAct[0].bouton.pack_forget()
            self.listeActPrec.append(self.listeAct.pop(0))

            try:
                self.listeAct.append(self.listeActSuiv.pop(0))
            except IndexError:
                pass

        self.ActuAction()

    def ActionDepG(self):
        """Methode  de la class niveau
        Deplace les action vers la gauche
        """
        listeTemp=[]
        self.listeAct[0].bouton.config(bg='white')
        for i in range(31,41):

            try:
                self.listeAct[30].bouton.pack_forget()
                listeTemp.append(self.listeAct.pop(30))
            except IndexError:
                pass

        self.listeActSuiv=listeTemp+self.listeActSuiv
        listeTemp=[]

        for i in range(0,10):
            try:
                listeTemp.append(self.listeActPrec.pop())
            except IndexError:
                pass

        listeTemp.reverse()
        self.listeAct=listeTemp+self.listeAct
        self.ActuAction()

    def DelAct(self, si=0, action=True):
        """Metode de la class niveau
        Supprime laction passe en parametre
        """
        if action != True:
            if action.action=='Avancer':
                intTemp = int(self.varnbAvancer.get())
                if si == 0:
                    if intTemp>=0:
                        intTemp+=1
                        self.varnbAvancer.set(intTemp)
                        self.ActuNBAct()

            elif action.action=='TournerG':
                intTemp = int(self.varnbTournerG.get())
                if si == 0:
                    if intTemp>=0:
                        intTemp+=1
                        self.varnbTournerG.set(intTemp)
                        self.ActuNBAct()

            elif action.action=='TournerD':
                intTemp = int(self.varnbTournerD.get())
                if si == 0:
                    if intTemp>=0:
                        intTemp+=1
                        self.varnbTournerD.set(intTemp)
                        self.ActuNBAct()

            elif action.action=='TakeDrop':
                intTemp = int(self.varnbTakeDrop.get())
                if si == 0:
                    if intTemp>=0:
                        intTemp+=1
                        self.varnbTakeDrop.set(intTemp)
                        self.ActuNBAct()

            action.bouton.pack_forget()
            self.listeAct.remove(action)

            try:
                self.listeAct.append(self.listeActSuiv.pop(0))
            except IndexError:
                pass

            if len(self.listeAct)>0:
                self.ActuAction()

            else:
                self.boutonStart.config(state='disabled')

            if len(self.listeAct)<31 and len(self.listeActPrec)>0:
                self.ActionDepG()

        else:
            for action in self.listeAct:
                action.bouton.pack_forget()

            self.listeAct=[]
            self.boutonStart.config(state='disabled')

    def Start(self):
        """Methode de la class niveau
        met les actions au debut
        et utilise la fonction move
        Si le perso fin sur la case fin, lance self.Fin
        sinon, lance self.Reinitialise
        """
        tempInt=len(self.listeActPrec)//10
        while tempInt>0:
            self.ActionDepG()
            tempInt-=1

        self.listeAFaire=self.listeAct+self.listeActSuiv
        self.Move()

        case=self.listeRangee[self.perso.posH].listeCase[self.perso.posL]
        if case.case.img==11:
            self.Fin()

        elif case.case.img==9:
            self.Reinitialise()

        elif self.mode==1:
            self.Reinitialise()

    def Move(self):
        """Methode de la class niveau
        Effectue les actions demander
        """
        vide=False
        while len(self.listeAFaire)>0:
            act=self.listeAFaire[0]

            if act.action=='Avancer':
                self.perso.Avancer()
                has=randint(1,5)
                if has==1:
                    self.interfacePar.bliblison["Bruit"]["sonChenille"].play()

            elif act.action=='TournerG':
                self.perso.TournerG()
                has=randint(1,5)
                if has==1:
                    self.interfacePar.bliblison["Bruit"]["sonChenille"].play()

            elif act.action=='TournerD':
                self.perso.TournerD()
                has=randint(1,5)
                if has==1:
                    self.interfacePar.bliblison["Bruit"]["sonChenille"].play()

            elif act.action=='TakeDrop':
                self.TakeDrop()

            case=self.listeRangee[self.perso.posH].listeCase[self.perso.posL]

            if case.case.img==3:
                case.liaison.Actione()
                case.Actione()

            elif case.case.img==3.2 and act.action=='Avancer':
                case.liaison.Actione()
                case.Actione()

            if case.case.img==9:
                vide=True
                self.Actualise()
                self.DelAct(1)
                del self.listeAFaire
                self.interfacePar.bliblison["Bruit"]["chute"].play()

                self.fenetre.update()
                self.fenetre.after(500)
                break

            else:
                self.Actualise()
                self.DelAct(1,self.listeAct[0])
                self.listeAFaire.remove(act)

                self.fenetre.update()
                self.fenetre.after(500)


class Rangee(Frame): #Herite de Frame
    """Class de rangee(frame)
    cree une rangee et une case
    demande un parent
    possede:
        -une liste de case
        -un parent
    """
    def __init__(self, parent):
        self.parent=parent

        Frame.__init__(self, self.parent) #Constructeur de Frame
        self.pack(side=TOP)
        self.propagate(1)

        self.listeCase=[]

class Case(Canvas): #Herite de Canvas
    """Class case(canvas)
    cree une case avec son image associer
    demande un parent, une rangee et une case de la carte
    possede:
        -un parent
        -une rangee
        -une case de la carte
    """
    def __init__(self, parent, rangee, case):
        self.parent=parent
        self.rangee=rangee
        self.case=case

        Canvas.__init__(self, self.rangee, highlightthickness=0,bd=0, height=50, width=50) #Constructeur canvas
        self.pack(side=LEFT)

        self.liaison=''

        #Ajout de l'image
        if case.img == 0:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgSol)

        elif case.img == 1:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgPontFN, tag='PontFN')

        elif case.img == 2:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgPontFO, tag='PontFO')

        elif case.img == 3:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgBoutonJO, tag='BoutonJO')

        elif case.img == 4:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgBoutonBO)

        elif case.img == 5:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgStBoite)

        elif case.img == 6:
            self.create_image(25, 25, image=self.parent.carte.ressources.img6)

        elif case.img == 7:
            self.create_image(25, 25, image=self.parent.carte.ressources.img7)

        elif case.img == 8:
            self.create_image(25, 25, image=self.parent.carte.ressources.img8)

        elif case.img == 9:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgVide)

        elif case.img == 10:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgStart)

        elif case.img == 11:
            self.create_image(25, 25, image=self.parent.carte.ressources.imgEnd)

    def Actione(self):
        """Methode de la class Case
        Effectue l'action correspondant
        et change l'image
        """
        if self.case.img == 1:
            self.delete('PontFN')
            self.create_image(25, 25, image=self.parent.carte.ressources.imgPontON, tag='PontON')
            self.case.img=1.2

        elif self.case.img == 1.2:
            self.delete('PontON')
            self.create_image(25, 25, image=self.parent.carte.ressources.imgPontFN, tag='PontFN')
            self.case.img=1

        elif self.case.img == 2:
            self.delete('PontFO')
            self.create_image(25, 25, image=self.parent.carte.ressources.imgPontOO, tag='PontOO')
            self.case.img=2.2

        elif self.case.img == 2.2:
            self.delete('PontOO')
            self.create_image(25, 25, image=self.parent.carte.ressources.imgPontFO, tag='PontFO')
            self.case.img=2

        elif self.case.img == 3:
            self.delete('BoutonJO')
            self.create_image(25, 25, image=self.parent.carte.ressources.imgBoutonJF, tag='BoutonJF')
            self.case.img=3.2

        elif self.case.img == 3.2:
            self.delete('BoutonJF')
            self.create_image(25, 25, image=self.parent.carte.ressources.imgBoutonJO, tag='BoutonJO')
            self.case.img=3


class Perso():
    """Class personnage
    demande et possede:
        -une position y
        -une position x
        -un orientation
    """
    def __init__(self, niveau, positionH, positionL , orientation='N'):
        self.posH=positionH
        self.posL=positionL
        self.orien=orientation
        self.porte=''
        self.niveau=niveau

    def Avancer(self):
        """Methode de la class Perso
        Verifie si le personnage peut avancer
        et si oui le fait
        """
        if self.orien=='N':
            caseSuiv=self.niveau.listeRangee[self.posH-1].listeCase[self.posL].case.img
            if caseSuiv==0 or caseSuiv==10 or caseSuiv==11 or caseSuiv==3 or caseSuiv==1.2 or caseSuiv==2.2 or caseSuiv==3.2 or caseSuiv==9:
                if self.posH!=0:
                    self.posH-=1
                    if self.porte!='':
                        self.porte.posH-=1

        elif self.orien=='E':
            try:
                caseSuiv=self.niveau.listeRangee[self.posH].listeCase[self.posL+1].case.img
                if caseSuiv==0 or caseSuiv==10 or caseSuiv==11 or caseSuiv==3 or caseSuiv==1.2 or caseSuiv==2.2 or caseSuiv==3.2 or caseSuiv==9:
                    if self.posL!=self.niveau.carte.l:
                        self.posL+=1
                        if self.porte!='':
                            self.porte.posL+=1

            except IndexError:
                pass

        elif self.orien=='S':
            try:
                caseSuiv=self.niveau.listeRangee[self.posH+1].listeCase[self.posL].case.img
                if caseSuiv==0 or caseSuiv==10 or caseSuiv==11 or caseSuiv==3 or caseSuiv==1.2 or caseSuiv==2.2 or caseSuiv==3.2 or caseSuiv==9:
                    if self.posH!=self.niveau.carte.h:
                        self.posH+=1
                        if self.porte!='':
                            self.porte.posH+=1

            except IndexError:
                pass

        elif self.orien=='O':
            caseSuiv=self.niveau.listeRangee[self.posH].listeCase[self.posL-1].case.img
            if caseSuiv==0 or caseSuiv==10 or caseSuiv==11 or caseSuiv==3 or caseSuiv==1.2 or caseSuiv==2.2 or caseSuiv==3.2 or caseSuiv==9:
                if self.posL!=0:
                    self.posL-=1
                    if self.porte!='':
                        self.porte.posL-=1

    def TournerD(self):
        """Methode de la class perso
        Fait tourner le personnage vers la droite
        """
        if self.orien=='N':
            self.orien='E'

        elif self.orien=='E':
            self.orien='S'

        elif self.orien=='S':
            self.orien='O'

        elif self.orien=='O':
            self.orien='N'

    def TournerG(self):
        """Methode de la class Perso
        Fait tourner le personnage vers la gauche
        """
        if self.orien=='N':
            self.orien='O'

        elif self.orien=='E':
            self.orien='N'

        elif self.orien=='S':
            self.orien='E'

        elif self.orien=='O':
            self.orien='S'

class Action():
    """Class action
    Enregistre l'action demander
    et l'ajoute a la liste
    demande l'action et le niveau
    possede:
        -le niveau(class)
        -l'action
        -l'image correspondant
    puis s'ajoute a la liste du niveau
    via la methode AddAction
    """
    def __init__(self, niveau, action):
        self.niveau=niveau
        self.action=action

        if self.action=='Avancer':
            self.img=self.niveau.imgTFlecheA

        elif self.action=='TournerG':
            self.img=self.niveau.imgTFlecheTG

        elif self.action=='TournerD':
            self.img=self.niveau.imgTFlecheTD

        elif self.action=='TakeDrop':
            self.img=self.niveau.imgTakeDrop

        elif self.action=='Sauter':
            self.img=self.niveau.imgTFlecheS

        self.bouton=Button(self.niveau,image=self.img, width=50, height=50, borderwidth=0, command=lambda: self.niveau.DelAct(0,self))
        self.niveau.AddAction(self)

class Boite():
    """Class Boite
    Cree un element boite
    possede:
        -le niveau(class)
        -une position en H
        -une position en L
    """
    def __init__(self, niveau, positionH, positionL):
        self.niveau=niveau
        self.posH=positionH
        self.posL=positionL

chemin="Core/Ressources/Interface/"
chemin1='Core/Ressources/Interface/manuel/'
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
        self.BoutonManuelRobot = Button(self.frameAcceuilManuel, image=self.ImageManuelRobot,width=155, height=70, command=self.RobotMAnuel )
        self.BoutonManuelRobot["bg"]="black"
        self.BoutonManuelRobot["fg"]="white"
        self.BoutonManuelRobot.place(x=450,y=200)

        self.ImageManuelTerrain= PhotoImage(file=chemin1+'terrain.gif')           #Bouton manuel terrain
        self.BoutonManuelTerrain = Button(self.frameAcceuilManuel, image=self.ImageManuelTerrain,width=155, height=70, command=self.TerrainManuel )
        self.BoutonManuelTerrain["bg"]="black"
        self.BoutonManuelTerrain["fg"]="white"
        self.BoutonManuelTerrain.place(x=450,y=300)

        self.ImageManuelAction= PhotoImage(file=chemin1+'action.gif')           #Bouton manuel action
        self.BoutonManuelAction = Button(self.frameAcceuilManuel, image=self.ImageManuelAction,width=155, height=70, command=self.ActionManuel )
        self.BoutonManuelAction["bg"]="black"
        self.BoutonManuelAction["fg"]="white"
        self.BoutonManuelAction.place(x=450,y=400)

        self.BoutonRetour = Button(self.frameAcceuilManuel, image=self.ImageBouton5,width=80, height=30, command=self.FonctionRetour)
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

        self.BoutonRetour = Button(self.frameRobotManuel, image=self.ImageBouton5,width=80, height=30, command=self.AcceuilManuel)
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

        self.ImageTexteArriver= PhotoImage(file=chemin1+'texte depart.gif',master=self)    # Image Texte Arriver
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

        self.ImageTexteVide= PhotoImage(file=chemin1+'texte sol.gif',master=self)    # Image Texte vide
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

        self.ImageTextebarierre= PhotoImage(file=chemin1+'texte sol.gif',master=self)    # Image Texte barierre
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

        self.BoutonRetour = Button(self.frameTerrainManuel, image=self.ImageBouton5,width=80, height=30, command=self.AcceuilManuel)
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
        self.BoutonSuivant1 = Button(self.frameTerrainManuel2, image=self.ImageSuivant1,width=45, height=45, command=self.Suivant1 )
        self.BoutonSuivant1["bg"]="black"
        self.BoutonSuivant1["fg"]="white"
        self.BoutonSuivant1.place(x=475,y=580)

        self.BoutonRetour = Button(self.frameTerrainManuel2, image=self.ImageBouton5,width=80, height=30, command=self.AcceuilManuel)
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

        self.BoutonRetour = Button(self.frameActionManuel, image=self.ImageBouton5,width=80, height=30, command=self.AcceuilManuel)
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

#-------------------------------------------------------------------------------
# Name:        ModuleMappeur
# Purpose:     Module de class concernant le mappeur du logiciel Objectif_Terre
#
# Author:      Guillaume Lebegue
#
# Copyright:   (c) ikkino 2018
#-------------------------------------------------------------------------------

##Importation des modules necessaires-------------------------------------------
from tkinter import *
from tkinter.messagebox import *
import Core.Bin.ModuleCarte
import os
import Core.Bin.ModulePrincipale as ModulePrincipale

##Class-------------------------------------------------------------------------
class Interface(Frame): #Herite de la class Frame du module tkinter
    """interface du logicielle de mapping
    herite de Frame de tkinter
    Possede:
        -Une fenetre mere
        -Une carte
        -Une bare de menu
        -Une liste de rangee grahique(frame)
        -Une MapACharge
    A pour fonctions:
        -Nouveau
        -Ouvrir
        -Charge
        -Select
        -Suppr
        -GenereRangee
        -GenereBouton
        -Save
    """
    def __init__(self,fenetre,bliblison,interfacePrec,mode=0, **kwargs):
        """Cree une interface
        Demande la fenetre parent"""
    ##Base--------------------------------------------------------------------------
        self.fenetre=fenetre #Fenetre parent
        Frame.__init__(self, self.fenetre, width=1000, height=650, bd=10, **kwargs)#Frame principal
        self.pack(fill=BOTH)#Remplit la fenetre
        self.pack_propagate(0)#Empeche la redefinition de la fenetre sur les widget interne
        self.listeRangee=[] #Liste de rangee graphique
        self.MapACharge="" #Varible remplit puis videe lors de l'apel de la methode ouvrir
        self.mode=mode
        self.bliblison=bliblison
        self.interfacePrec=interfacePrec

    ##Generation de la carte--------------------------------------------------------
        if self.mode == 0:
            self.carte=Core.Bin.ModuleCarte.Map(1) #Carte
        elif self.mode == 1:
            self.carte=Core.Bin.ModuleCarte.Map()


        ##Menu--------------------------------------------------------------------------
        self.menuBar=Menu(self.fenetre) #Menu

        self.menuBar.add_command(label="Ouvrir", command=self.Ouvrir) #Bouton liee a la methode Ouvir
        self.menuBar.add_command(label="Nouveau", command=self.Nouveau) #Bouton liee a la methode Nouveau
        self.menuBar.add_command(label="Enregistrer", command=self.Save) #Bouton liee a la methode Save
        self.menuBar.add_command(label="Supprimer", command=self.Suppr) #Bouton liee a la methode Suppr
        self.menuBar.add_command(label="Options", command=self.Options) #Bouton liee a la methode Option
        self.menuBar.add_command(label="Histoire Precedent", command=lambda: FenHistoire(self,0)) #Bouton liee a la methode Histoire, lui envoi 0
        self.menuBar.add_command(label="Histoire Suivant", command=lambda: FenHistoire(self,1)) #Bouton liee a la methode Histoire, lui envoi 1
        self.menuBar.add_command(label="Quitter", command=self.Quitter)

        self.fenetre.config(menu=self.menuBar) #Config le menu pour aparaitre sur la fenetre

    def Nouveau(self):
        """Methode de l'interface
        Cree une nouvel carte
        """
        if self.carte.l==0 or self.carte.h==0: #Verifie si une carte est deja charge
            self.carte.CreeNouv(self) #Utilise la fonction
            self.Charge() #Utilise la methode

        elif self.carte.sauvegarder==False: #Si la map n'a pas ete sauvegarder
            if askyesno("Nouveau ?","La carte n'a pas ete sauvegarde, en cree une nouvelle ?"): #Si non, demande si on veut la sauvegarder
                for i in self.listeRangee: #Pour chaque rangee graphique
                    i.destroy() #Les detruires
                self.listeRangee=[] #Remetre a 0 la liste de rangee
                self.pack_propagate(0) #Empeche la redefinition automatique
                if self.mode == 0:
                    self.carte=Core.Bin.ModuleCarte.Map(1) #Cree un nouvel objet de type Map
                elif self.mode == 1:
                    self.carte=Core.Bin.ModuleCarte.Map()
                self.carte.CreeNouv(self) #Fonction
                self.Charge() #Methode

        elif self.carte.sauvegarder==True: #Si la map a ete sauvegarder
            for i in self.listeRangee: #pour chaque rangee graphique
                i.destroy() #Les detruires
            self.listeRangee=[] #Remettre a 0 la liste de rangee
            self.pack_propagate(0) #Empeche la redefinition automatique
            if self.mode == 0:
                self.carte=Core.Bin.ModuleCarte.Map(1) #Cree un nouvel objet de type Map
            elif self.mode == 1:
                self.carte=Core.Bin.ModuleCarte.Map()
            self.carte.CreeNouv(self) #Fonction
            self.Charge() #Methode

    def Ouvrir(self):
        """Methode de l'interface
        Ouvre une Map preenregistrer
        et la charge
        """
        if self.carte.l==0 or self.carte.h==0: #Verifie si une carte est deja charge
            FenetreCharge(self) #Ouvre une fenetre de selection
            if self.MapACharge != "": #Si la selection n'est pas vide
                if self.mode == 1:
                    self.carte=Core.Bin.ModuleCarte.Ouvrir(self.MapACharge) #Charge la Map depuis la focntion prevu
                elif self.mode == 0:
                    self.carte=Core.Bin.ModuleCarte.Ouvrir(self.MapACharge,1) #Charge la Map depuis la focntion prevu
                self.MapACharge="" #Reinitialise la variable
                self.carte.ressources=Core.Bin.ModuleCarte.Ressources(self.carte.biome) #Charge les ressources
                self.Charge() #Effectue la chargement graphique de l'interface

        elif self.carte.sauvegarder==False: #Si la map n'a pas ete sauvegarder
            if askyesno("Ouvrir ?","La carte n'a pas ete sauvegarde, la remplacer ?"): #Si non, demande si on veut la sauvegarder
                for i in self.listeRangee: #Pour chaque rangee graphiques
                    i.destroy() #Les detruires
                self.listeRangee=[] #Reinitialise la liste de rangee
                self.pack_propagate(0) #Empeche la redefinition automatique

                FenetreCharge(self) #Ouvre une fenetre de selection
                if self.MapACharge != "": #Si la selection n'est pas vide
                    if self.mode == 1:
                        self.carte=Core.Bin.ModuleCarte.Ouvrir(self.MapACharge) #Charge la Map depuis la focntion prevu
                    elif self.mode == 0:
                        self.carte=Core.Bin.ModuleCarte.Ouvrir(self.MapACharge,1) #Charge la Map depuis la focntion prevu
                    self.MapACharge="" #Reinitialise la variable
                    self.carte.ressources=Core.Bin.ModuleCarte.Ressources(self.carte.biome) #Charge les ressources
                    self.Charge() #Effectue la chargement graphique de l'interface

        elif self.carte.sauvegarder==True: #Si la map a ete sauvegarder
            for i in self.listeRangee: #Pour chaque rangee graphiques
                i.destroy() #Les detruires
            self.listeRangee=[] #Reinitialise la liste
            self.pack_propagate(0) #Empeche la redefinition automatique

            FenetreCharge(self) #Ouvre une fenetre de selection
            if self.MapACharge != "": #Si la selection n'est pas vide
                if self.mode == 1:
                    self.carte=Core.Bin.ModuleCarte.Ouvrir(self.MapACharge) #Charge la Map depuis la focntion prevu
                elif self.mode == 0:
                    self.carte=Core.Bin.ModuleCarte.Ouvrir(self.MapACharge,1) #Charge la Map depuis la focntion prevu
                self.MapACharge="" #Reinitialise la variable
                self.carte.ressources=Core.Bin.ModuleCarte.Ressources(self.carte.biome) #Charge les ressources
                self.Charge() #Effectue la chargement graphique de l'interface

    def Quitter(self):
        if self.mode == 0:
            self.pack_forget()
            self.interfacePrec.pack()
            self.menuBar.destroy()
            self.destroy()
        elif self.mode == 1:
            self.fenetre.destroy()

    def Charge(self):
        """Affiche les cases de la map
        sous forme de bouton
        """

        for i in self.carte.listerangee: #Pour chaque rangee de la carte
            self.GenereRangee() #Cree une rangee
        u=0
        for rangee in self.listeRangee:
            for e in self.carte.listerangee[u].listecase: #Pour chaque case de la rangee
                self.GenereBouton(rangee, e) #Cree une case dans la rangee
            u+=1
        self.propagate(0) #Autorise la propagation !!!

    def Select(self, case, bouton):
        """Fonction de l'interface
        Demande une case et un bouton
        et l'envoi lors de la creation de
        InterfaceSelect
        Puis, a la fin de l'interface, remplace l'image
        """
        interfaceSelect = InterfaceSelect(self, case) #InterfaceSelect
        for rangee in self.listeRangee :
            rangee.destroy()
        self.listeRangee=[]
        self.Charge()

    def Suppr(self):
        """Fonction Supprimant la carte actuel
        Demande si on veut aussi supprimer le fichier, si il existe
        """
        if askyesno("Suppression ?","Reinitialiser la carte ?"): #Question oui/non du module tkinter.messageBox
            chemin=self.carte.chemin #Recupere le chemin de la carte dans une variable temporaire
            num=self.carte.num #Recupere le num de la carte dans une variable temporaire
            del(self.carte) #Detruis la carte

            for i in self.listeRangee: #Pour chaque rangee graphique
                i.destroy() #Les detruires

            self.listeRangee=[] #Reinitialise la liste de rangee
            self.pack_propagate(0) #Empeche la redefinition automatique
            self.carte=Core.Bin.ModuleCarte.Map() #Cree une nouvelle carte

            fichierTrouve = False
            if self.mode == 1:
                for fichier in os.listdir('Core/Map'): #Pour chaques fichier dans la liste
                    if num == fichier: #Si il esxiste deja un fichier
                        fichierTrouve = True
            elif self.mode== 0:
                for fichier in os.listdir('Carte-Cree'): #Pour chaques fichier dans la liste
                    if num == fichier: #Si il esxiste deja un fichier
                        fichierTrouve = True

            if fichierTrouve:
                if askyesno("Suppression ?","Supprimer le fichier ?"): #Question oui/non du module tkinter.messageBox
                    os.remove(chemin) #Supprime le fichier

    def Options(self):
        """Methode de l'interface
        Si la carte a un biome
        ouvre une fenetre des options
        """
        if self.carte.biome!="":
            FenetreOption(self)

    def GenereRangee(self):
        """Fonction de l'interface
        creant des rangee de la carte
        """
        frame = Frame(self) #Cree une nouvelle rangee graphique
        frame.pack(side=TOP)
        frame.propagate(1)
        self.listeRangee.append(frame) #Ajout a la liste de rangee

    def GenereBouton(self, rangee, case):
        """Fonction de l'interface
        creant un bouton de la carte
        recupere l'image d'une case
        demande une rangee graphique parent
        et la case correspondant au boutton
        """
        if case.img == 0:
            bouton = Button(rangee, image=self.carte.ressources.imgSol, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 1:
            bouton = Button(rangee, image=self.carte.ressources.imgPontFN, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 2:
            bouton = Button(rangee, image=self.carte.ressources.imgPontFO, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 3:
            bouton = Button(rangee, image=self.carte.ressources.imgBoutonJO, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 4:
            bouton = Button(rangee, image=self.carte.ressources.imgBoutonBO ,highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 5:
            bouton = Button(rangee, image=self.carte.ressources.imgStBoite, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 6:
            bouton = Button(rangee, image=self.carte.ressources.img6, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 7:
            bouton = Button(rangee, image=self.carte.ressources.img7, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 8:
            bouton = Button(rangee, image=self.carte.ressources.img8, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 9:
            bouton = Button(rangee, image=self.carte.ressources.imgVide, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 10:
            bouton = Button(rangee, image=self.carte.ressources.imgStart, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

        elif case.img == 11:
            bouton = Button(rangee, image=self.carte.ressources.imgEnd, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case, bouton))
            bouton.pack(side=LEFT)

    def Save(self):
        """Methode de l'interface appelant la methode Save de sa carte
        Verifie la presence d'une case start et end
        """
        start=0
        end=0
        for rangee in self.carte.listerangee: #Pour chaques rangee dans la liste
            for case in rangee.listecase: #Pour chaques case dans la liste de case de la rangee
                if case.img==10: #Si la case est start
                    start+=1

                elif case.img==11: #Si la case est end
                    end+=1

        if start!=1: #Si il y a pas ou plus d'une case start
            showerror("Probleme de case","Vous avez {} case de depart(S), 1 nescessaire".format(start)) #Fenetre du module tkinter.messageBox

        elif end != 1: #Si il y a pas ou plus d'une case end
            showerror("Probleme de case","Vous avez {} case d'arrive(E), 1 nescessaire".format(end)) #Fenetre du module tkinter.messageBox

        else: #Si aucun probleme
            showinfo("Enregistrement","Pour enregistrer la nouvelle carte,\nveuillez tester et reussir la carte")
            self.carte.Save()
            self.FenTest=Toplevel(self)
            niveau=ModulePrincipale.Niveau(self.FenTest,self.carte.num,self,1,1)

    def Suite(self,result,nbNiveau=""):
        if result == 0:
            self.FenTest.destroy()
            os.remove(self.carte.chemin)
            self.fenetre.destroy()
        elif result == 1:
            self.FenTest.destroy()
            os.remove(self.carte.chemin)
            showinfo("Rate","Vous n'avez pas reussi a finir le niveau.\nAinsi, le niveau n'est pas enregistre")
        elif result == 2:
            self.FenTest.destroy()
            self.carte.sauvegarder=True #Variable de la carte
            showinfo("Sauvegarde","Sauvegarde reussi !")

class InterfaceSelect(Toplevel): #Herite de Toplevel du module tkinter
    """Interface d'une fenetre de selection du logicielle de mapping
    Demande un parent et une case
    Possede:
        -Une frame principale
        -Une case
        -Un biome
        -Des ressources
        -Des rangee
        -Des boutons
    A pour fonction:
        -Select
    """
    def __init__(self, master, case, **kwargs):
        """Cree une interface de selection
        demande un parent et une case"""
        self.master = master

        Toplevel.__init__(self, self.master) #Constructeur de la class Toplevel
        self.frame = Frame(self, bd=10, **kwargs) #Frame principale
        self.frame.pack(fill=BOTH)
        self.frame.pack_propagate(1) #Autorise la redefinition automatique !!!

        self.case=case #Case
        self.biome=self.master.carte.biome #Biome = Biome de la case
        self.ressources=Core.Bin.ModuleCarte.Ressources(self.biome) #Ressources chargee a partir du biome
        self.liaison=''

        ##Rangee----------------------------------------------------------------
        self.rangee1 = Frame(self.frame) #Rangee
        self.rangee1.pack(side=TOP)

        self.rangee2 = Frame(self.frame) #Rangee
        self.rangee2.pack(side=TOP)

        self.rangee3 = Frame(self.frame) #Rangee
        self.rangee3.pack(side=TOP)

        ##Boutons---------------------------------------------------------------
        self.bouton1 = Button(self.rangee1, height=50 , width=50, image=self.ressources.imgPontFN, command=lambda : self.Select(1)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton1.pack(side=LEFT)

        self.bouton2 = Button(self.rangee1, height=50 , width=50, image=self.ressources.imgPontFO, command=lambda : self.Select(2)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton2.pack(side=LEFT)

        self.bouton3 = Button(self.rangee1, height=50 , width=50, image=self.ressources.imgBoutonJO, command=lambda : self.Select(3)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton3.pack(side=LEFT)

        self.bouton4 = Button(self.rangee2, height=50 , width=50, image=self.ressources.imgBoutonBO, command=lambda : self.Select(4)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton4.pack(side=LEFT)

        self.bouton5 = Button(self.rangee2, height=50 , width=50, image=self.ressources.imgStBoite, command=lambda : self.Select(5)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton5.pack(side=LEFT)

        self.bouton6 = Button(self.rangee2, height=50 , width=50, image=self.ressources.img6, command=lambda : self.Select(6)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton6.pack(side=LEFT)

        self.bouton7 = Button(self.rangee3, height=50 , width=50, image=self.ressources.img7, command=lambda : self.Select(7)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton7.pack(side=LEFT)

        self.bouton8 = Button(self.rangee3, height=50 , width=50, image=self.ressources.img8, command=lambda : self.Select(8)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton8.pack(side=LEFT)

        self.bouton9 = Button(self.rangee3, height=50 , width=50, image=self.ressources.imgVide, command=lambda : self.Select(9)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton9.pack(side=LEFT)

        self.bouton10 = Button(self.frame, height=50 , width=50, image=self.ressources.imgStart, command=lambda : self.Select(10)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton10.pack(side=LEFT)

        self.bouton0 = Button(self.frame, height=50 , width=50, image=self.ressources.imgSol, command=lambda : self.Select(0)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton0.pack(side=LEFT)

        self.bouton11 = Button(self.frame, height=50 , width=50, image=self.ressources.imgEnd, command=lambda : self.Select(11)) #Bouton liee a Select, lui envoi le numero du bouton
        self.bouton11.pack(side=LEFT)

        ##Parametrage Toplevel--------------------------------------------------
        self.transient() #Definie fenetre secondaire
        self.grab_set()
        self.focus_set() #Regle le focus sur la fenetre
        self.wait_window() #Gel le reste du programe

    def Select(self, selection):
        """Fonction de la class InterfaceSelect
        Demande la selection
        modifie la variable Img de la case
        """
        if self.case.img == 1 or self.case.img == 2:
            listeCaseLiais=[]
            for rangee in self.master.carte.listerangee:
                for case in rangee.listecase:
                    if case.liaison == self.case:
                        listeCaseLiais.append(case)
            if listeCaseLiais != []:
                if askyesno("Suppression pont","Vous voulez supprimer un pont.\nMais ce pont est lié à des boutons.\nSi vous supprimer le pont, les boutons le seront aussi.\nEtes vous sur ?"):
                    for case in listeCaseLiais:
                        case.img=0
                        case.liaison=""
                    self.case.img=selection
                    self.destroy()
                else:
                    self.destroy()
            else:
                self.case.img=selection
                if selection==3 or selection==4:
                    self.Liaison()
                else:
                    self.case.liaison=""

                self.destroy() #Detrui la fenetre
        else:
            self.case.img=selection
            if selection==3 or selection==4:
                self.Liaison()
            else:
                self.case.liaison=""

            self.destroy() #Detrui la fenetre

    def Liaison(self):
        """Methode de la class InterfaceSelect
        Ouvre une fenetre de liaison
        puis assigne le resultat a la case
        """
        liaison=FenetreLiaison(self)
        self.case.liaison=self.liaison


class FenetreLiaison(Toplevel):
    """Class heritant de Toplevel
    Interface de selection de liaison du mappeur
    Affiche une copie de la carte avec les cases en tant que des boutons
    selectione la case de liaison en cliquant
    demande un parent et par son biais obtient la case a modifier
    possede:
        -un parent
        -une liste de rangee
        -des elements graphiques
    a pour fonction:
        -Select
        -Annuler
        -GenereRangee
        -GenereBouton
    """
    def __init__(self,master):
        """Methode de la class FenetreLiaison
        demande un parent et cree une interface
        """
        self.master=master

        Toplevel.__init__(self, self.master, width=1000, height=650, bd=10) #Genere le Toplevel
        self.pack_propagate(0) #Empeche la redefinition
        self.listeRangee=[]

        self.QueFaire=Label(self,text='Selectionner case a lier',font=("Helvetica", 16)) #Label posedant une police speciale
        self.QueFaire.pack(side=TOP)

        u=0
        for i in self.master.master.carte.listerangee: #Pour chaque rangee de la carte
            self.GenereRangee() #Cree une rangee
            for e in i.listecase: #Pour chaque case de la rangee
                self.GenereBouton(self.listeRangee[u], e) #Cree une case dans la rangee
            u+=1

        self.BoutonQuitter=Button(self,text='Annuler',font=("Helvetica", 16),command=self.Annuler) #Bouton posedant une police speciale liee a Annuler
        self.BoutonQuitter.pack(side=BOTTOM)

        self.protocol("WM_DELETE_WINDOW", self.Annuler) #Si on ferme la fenetre, faire Annuler
        self.transient() #Definie fenetre secondaire
        self.grab_set()
        self.focus_set() #Regle le focus sur la fenetre
        self.wait_window() #Gel le reste du programe

    def Select(self, case):
        """Methode de la class FenetreLiaison
        Demande la case selectioner
        et la remplace dans la variable liaison du parent
        si la case selectionner est un pont
        sinon montre un message d'erreur
        """
        nbcase=case.img # =type de la case

        if nbcase==1 or nbcase==2: #Si case est un pont
            self.master.liaison=case #Enregistrer la case dans la variable du parent
            self.destroy() #Detruit la fenetre

        else:
            showerror('Mauvaise case', 'Choisissez une case valide(pont)') #Message d'erreur

    def Annuler(self):
        """Fonction de la class FenetreLiaison
        Enregistre rien sur la variable liaison du parent
        puis ferme le Toplevel car son parent se ferme
        """
        self.master.liaison=''
        self.master.Select(0)

    def GenereRangee(self):
        """Fonction de l'interface
        creant des rangee de la carte
        """
        frame = Frame(self) #Cree une nouvelle rangee graphique
        frame.pack(side=TOP)
        frame.propagate(1)
        self.listeRangee.append(frame)

    def GenereBouton(self, rangee, case):
        """Fonction de l'interface
        creant un bouton de la carte
        recupere l'image d'une case
        demande une rangee graphique parent
        et la case correspondant au boutton
        """
        if case.img == 0:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgSol, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 1:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgPontFN, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 2:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgPontFO, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 3:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgBoutonJO, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 4:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgBoutonBO ,highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 5:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgStBoite, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 6:
            bouton = Button(rangee, image=self.master.master.carte.ressources.img6, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 7:
            bouton = Button(rangee, image=self.master.master.carte.ressources.img7, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 8:
            bouton = Button(rangee, image=self.master.master.carte.ressources.img8, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 9:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgVide, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 10:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgStart, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)

        elif case.img == 11:
            bouton = Button(rangee, image=self.master.master.carte.ressources.imgEnd, highlightthickness=0,bd=0, height=50, width=50, command=lambda : self.Select(case))
            bouton.pack(side=LEFT)


class FenetreCharge(Toplevel): #Herite de la class Toplevel de tkinter
    """Class ouvrant une fenetre secondaire
    demande a la selection une liste de carte
    charge automatiquement les cartes depuis Core/Map
    Possede:
        -Un parent
        -Une liste de nom de fichier de carte
        -Une frame principale
        -Un boutton Ok
    A pour fonction:
        -Select Fonction appeler lors du clic boutton ou close fenetre, renvoi la carte selectionner
        """
    def __init__(self, master):
        """Cree une fenetre de selection de carte
        demande le parent
        """
        Toplevel.__init__(self) #Constructeur d'une fenetre secondaire

        self.master=master #Parent

        if self.master.mode == 1:
            self.listeFichMap = os.listdir('Core/Map') #Liste de nom de fichier
        elif self.master.mode == 0:
            self.listeFichMap = os.listdir('Carte-Cree') #Liste de nom de fichier
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
            showerror("Aucun fichier","Aucun fichier n'a ete trouve") #Fenetre du module tkinter.messageBox
            self.destroy()

    def Select(self):
        """Fonction de la class FenetreCharge
        Recupere la selection et l'enregistre
        """
        self.master.MapACharge = self.listeMap.get(self.listeMap.curselection()) #Recupere la selection et la modifie sur le parent
        self.destroy() #Ferme la fenetre


class FenetreOption(Toplevel):
    """Class heritant de Toplevel
    Ouvre une fenetre avec plusieurs options
    posede:
        -un parent
        -une orientation
        -des widgets
    a pour fonction:
        -CheckBox
        -CallAvancer
        -CallTournerG
        -CallTournerD
        -CallTakeDrop
        -CallBox
        -Enregistrer
        -Quitter
    """
    def __init__(self, master):
        """Methode de la class FenetreOption
        demande un parent
        initialise le Toplevel
        """
        Toplevel.__init__(self) #Cree le Toplevel

        self.master=master
        self.orien=master.carte.oriPers #Orientation du perso

    ##Elements graphiques-------------------------------------------------------
        ##CheckBox orientation--------------------------------------------------
        self.FrameOrien=Frame(self)
        self.FrameOrien.pack(fill=X,side=TOP)

        self.CheckOrienN=Checkbutton(self.FrameOrien, text='N', command=lambda : self.CheckBox('N'))
        self.CheckOrienN.pack(side=LEFT)

        self.CheckOrienS=Checkbutton(self.FrameOrien, text='S', command=lambda : self.CheckBox('S'))
        self.CheckOrienS.pack(side=LEFT)

        self.CheckOrienO=Checkbutton(self.FrameOrien, text='O', command=lambda : self.CheckBox('O'))
        self.CheckOrienO.pack(side=LEFT)

        self.CheckOrienE=Checkbutton(self.FrameOrien, text='E', command=lambda : self.CheckBox('E'))
        self.CheckOrienE.pack(side=LEFT)

        ##Nombre d'action-------------------------------------------------------
        self.frameNB=Frame(self, bd=1, relief=RAISED)
        self.frameNB.pack(fill=X,side=TOP)
        self.labelFrameNB1=Label(self.frameNB, text="Nombre d'action autoriser")
        self.labelFrameNB1.pack(side=TOP)
        self.labelFrameNB2=Label(self.frameNB, text="(0=Aucune/-1=Infini)")
        self.labelFrameNB2.pack(side=TOP)

        self.frameNBAvancer=Frame(self.frameNB)
        self.frameNBAvancer.pack(fill=X,side=TOP)
        self.labelNBAvancer=Label(self.frameNBAvancer,text="Avancer")
        self.labelNBAvancer.pack(side=LEFT)
        self.varNBAvancer=StringVar(self, self.master.carte.nbAvancer)
        self.varNBAvancer.trace('w',self.CallAvancer)
        self.textNBAvancer=Entry(self.frameNBAvancer,textvariable=self.varNBAvancer)
        self.textNBAvancer.pack(side=RIGHT)


        self.frameNBTournerG=Frame(self.frameNB)
        self.frameNBTournerG.pack(fill=X,side=TOP)
        self.labelNBTournerG=Label(self.frameNBTournerG,text="Tourner a gauche")
        self.labelNBTournerG.pack(side=LEFT)
        self.varNBTournerG=StringVar(self, self.master.carte.nbTournerG)
        self.varNBTournerG.trace('w',self.CallTournerG)
        self.textNBTournerG=Entry(self.frameNBTournerG,textvariable=self.varNBTournerG)
        self.textNBTournerG.pack(side=RIGHT)

        self.frameNBTournerD=Frame(self.frameNB)
        self.frameNBTournerD.pack(fill=X,side=TOP)
        self.labelNBTournerD=Label(self.frameNBTournerD,text="Tourner a droite")
        self.labelNBTournerD.pack(side=LEFT)
        self.varNBTournerD=StringVar(self, self.master.carte.nbTournerD)
        self.varNBTournerD.trace('w',self.CallTournerD)
        self.textNBTournerD=Entry(self.frameNBTournerD,textvariable=self.varNBTournerD)
        self.textNBTournerD.pack(side=RIGHT)

        self.frameNBTakeDrop=Frame(self.frameNB)
        self.frameNBTakeDrop.pack(fill=X,side=TOP)
        self.labelNBTakeDrop=Label(self.frameNBTakeDrop,text="Take/Drop")
        self.labelNBTakeDrop.pack(side=LEFT)
        self.varNBTakeDrop=StringVar(self, self.master.carte.nbTakeDrop)
        self.varNBTakeDrop.trace('w',self.CallTakeDrop)
        self.textNBTakeDrop=Entry(self.frameNBTakeDrop,textvariable=self.varNBTakeDrop)
        self.textNBTakeDrop.pack(side=RIGHT)

        ##Boutons---------------------------------------------------------------
        self.frameBouton=Frame(self)
        self.frameBouton.pack(side=TOP)
        self.boutonAnnule=Button(self.frameBouton, text="Anuler", command=self.destroy)
        self.boutonAnnule.pack(side=LEFT)
        self.boutonEnregi=Button(self.frameBouton, text="Enregistrer", command=self.Enregistrer)
        self.boutonEnregi.pack(side=RIGHT)

    #Selectionne case default---------------------------------------------------
        if self.orien == 'N':
            self.CheckOrienN.select()
            self.CheckBox('N')

        elif self.orien == 'S':
            self.CheckOrienS.select()
            self.CheckBox('S')

        elif self.orien == 'O':
            self.CheckOrienO.select()
            self.CheckBox('O')

        else :
            self.CheckOrienE.select()
            self.CheckBox('E')

    ##Parametrage Toplevel------------------------------------------------------
        self.transient() #Declare fenetre secondaire
        self.grab_set()
        self.focus_set() #Focus de l'ecran
        self.wait_window() #Gele le reste du programe

    def CheckBox(self, box):
        """Deselectione les autres checkbox
        demande la checkbox selectionne
        """
        if box=='N': #Si box selectioner est N
            self.CheckOrienS.deselect() #Deselectione
            self.CheckOrienO.deselect() #Deselectione
            self.CheckOrienE.deselect() #Deselectione
            self.orien='N' #Modifie

        elif box=='S': #Si box selectioner est S
            self.CheckOrienN.deselect() #Deselectione
            self.CheckOrienO.deselect() #Deselectione
            self.CheckOrienE.deselect() #Deselectione
            self.orien='S' #Modifie

        elif box=='O': #Si box selectioner est O
            self.CheckOrienN.deselect() #Deselectione
            self.CheckOrienS.deselect() #Deselectione
            self.CheckOrienE.deselect() #Deselectione
            self.orien='O' #Modifie

        elif box=='E': #Si box selectioner est E
            self.CheckOrienN.deselect() #Deselectione
            self.CheckOrienS.deselect() #Deselectione
            self.CheckOrienO.deselect() #Deselectione
            self.orien='E' #Modifie

    def CallAvancer(self, *arg):
        """Methode de la class FenetreOption
        Appele la methode callback avec comme parametre varNBAvancer
        """
        self.CallBack(self.varNBAvancer)
    def CallTournerG(self, *arg):
        """Methode de la class FenetreOption
        Appele la methode callback avec comme parametre varNBTournerG
        """
        self.CallBack(self.varNBTournerG)
    def CallTournerD(self, *arg):
        """Methode de la class FenetreOption
        Appele la methode callback avec comme parametre varNBTournerD
        """
        self.CallBack(self.varNBTournerD)
    def CallTakeDrop(self, *arg):
        """Methode de la class FenetreOption
        Appele la methode callback avec comme parametre varNBTakeDrop
        """
        self.CallBack(self.varNBTakeDrop)

    def CallBack(self,var):
        """Methode de la class FenetreOption
        verifie l'entree des Entry
        empeche:
            -lettre
        demande une variable
        """
        contvar=var.get() #Recupere la variable
        contvar=contvar.replace(' ','')#Suppresion des espaces

        try:
            verifvarlist=[]
            for elem in contvar:
                if elem in ('0','1','2','3','4','5','6','7','8','9','-'):
                    verifvarlist.append(elem) #Ajoute que les nombres et -

        except IndexError:
            pass

        verifvar=''
        verifvar=verifvar.join(verifvarlist) #Transform en str
        var.set(verifvar) #Remplace

    def Enregistrer(self):
        """Methode de la class FenetreOption
        Verifie que les nombre sont >= -1
        puis enregistre
        """
        problnb=False #En cas de probleme passe a true

        nbAvancer=int(self.varNBAvancer.get())
        if nbAvancer<-1:
            problnb=True

        nbTournerG=int(self.varNBTournerG.get())
        if nbTournerG<-1:
            problnb=True

        nbTournerD=int(self.varNBTournerD.get())
        if nbTournerG<-1:
            problnb=True

        nbTakeDrop=int(self.varNBTakeDrop.get())
        if nbTakeDrop<-1:
            problnb=True

        if not problnb: #Si pas de brobleme
            self.master.carte.nbAvancer=self.varNBAvancer.get() #Remplace
            self.master.carte.nbTournerG=self.varNBTournerG.get() #Remplace
            self.master.carte.nbTournerD=self.varNBTournerD.get() #Remplace
            self.master.carte.nbTakeDrop=self.varNBTakeDrop.get() #Remplace
            self.master.carte.oriPers=self.orien #Remplace
            self.destroy() #Ferme

        else: #Si probleme
            showerror("Mauvaise valeur", "Vous avez entre une mauvaise valeur") #Message d'erreur


class FenHistoire(Toplevel):
    """Class heritant de Toplevel
    Ouvre une fenetre secondaire qui montres toutes les
    histoires enregistrer dans la map
    possede un parent, un mode et des widgets graphiques
    a pour fonction:
        -Nouveau
        -Supprimer
        -Modifier
    """
    def __init__(self, parent, mode):
        """Constructeur de la class FenHistoire
        demande un parent et un mode
        """
        Toplevel.__init__(self) #Constructeur Toplevel

        self.parent=parent
        self.mode=mode

        #Selection de la liste en fonction du mode
        if self.mode == 0:
            self.listeHistoire=self.parent.carte.histPrec

        elif self.mode == 1:
            self.listeHistoire=self.parent.carte.histSuiv

        #Boite de selection d'histoire
        self.listeHist = Listbox(self)
        self.listeHist.pack(side=TOP)

        for histoire in self.listeHistoire: #Pour chaque histoire dans la liste
            self.listeHist.insert(END, histoire) #Ajout a la boite de selection
        self.listeHist.selection_set( first = 0 ) #Selection par defaut

        self.frameBouton1=Frame(self)
        self.frameBouton1.pack(side=TOP)

        self.boutonNouv=Button(self.frameBouton1,text="Nouveau",command=self.Nouveau)
        self.boutonNouv.pack(side=LEFT)

        self.boutonModif=Button(self.frameBouton1,text="Modifier",command=self.Modifier)
        self.boutonModif.pack(side=LEFT)

        self.frameBouton2=Frame(self)
        self.frameBouton2.pack(side=TOP)

        self.boutonSupp=Button(self.frameBouton2, text="Supprimer",command=self.Supprimer)
        self.boutonSupp.pack(side=LEFT)

        self.boutonAnn=Button(self.frameBouton2,text="Fermer",command=self.destroy)
        self.boutonAnn.pack(side=LEFT)

        #Parametrage Toplevel
        self.transient() #Declare fenetre secondaire
        self.grab_set()
        self.focus_set() #Focus de l'ecran
        self.wait_window() #Gele le reste du programe

    def Nouveau(self):
        """Methode de la class FenHistoire
        Cree une nouvelle histoire vide
        qu'il ajoute a la fin de la liste
        puis actualise la listBox
        """
        hist=["-"] #Cree une nouvelle histoire
        self.listeHistoire.append(hist) #Ajout de l'histoire
        self.listeHist.delete(0,END) #Vide la listBox

        for histoire in self.listeHistoire: #Pour chaque histoire dans la liste
            self.listeHist.insert(END, histoire) #Ajout a la boite de selection
        self.listeHist.selection_set( first = 0 ) #Selection par defaut

    def Supprimer(self):
        """Methode de la class FenHistoire
        Supprime la list selectionner
        puis actualise la listBox
        """
        listaSup=list(self.listeHist.get(self.listeHist.curselection())) #Recupere la list selectionner (sous forme de liste)
        self.listeHist.delete(0,END) #Vide la listBox

        self.listeHistoire.remove(listaSup) #Retire de la liste

        for histoire in self.listeHistoire: #Pour chaque histoire dans la liste
            self.listeHist.insert(END, histoire) #Ajout a la boite de selection
        self.listeHist.selection_set( first = 0 ) #Selection par defaut

    def Modifier(self):
        """Methode de la class FenHistoire
        Recupere la selection
        et l'envoi a une nouvelle fenetre
        puis actualise la listBox
        """
        listBoxAModif=list(self.listeHist.get(self.listeHist.curselection())) #Recupere la selection

        #Recuperation de la liste precise
        for hist in self.listeHistoire:
            if hist == listBoxAModif:
                listAModif=hist

        #Creation de la fenetre supplementaire
        FenModifHist(self,listAModif)

        self.listeHist.delete(0,END) #Vide la listBox

        for histoire in self.listeHistoire: #Pour chaque histoire dans la liste
            self.listeHist.insert(END, histoire) #Ajout a la boite de selection
        self.listeHist.selection_set( first = 0 ) #Selection par defaut


class FenModifHist(Toplevel):
    """Class heritant de Toplevel
    recupere une liste dont il affiche le contenue
    dans des entry modifiables
    lors de l'enregistrement, modifie l'origine de la liste recu
    possede:
        -un parent
        -une liste a modifier
        -des widgets
    a pour fondtion:
        -Enregistrer
        -CallBack
    """
    def __init__(self,master,listAMod):
        """Constructeur de la class FenModifHist
        demande un parent et une list a modifier
        """
        self.master=master
        self.listAMod=listAMod

        Toplevel.__init__(self) #Constructeur Toplevel

        #Recupere les lignes de l'histoire si elles existent
        try:
            self.varLigne1=StringVar(self, value=self.listAMod[0]) #Cree un StringVar contenant la premiere ligne
        except IndexError: #Si la ligne n'existe pas
            self.varLigne1=StringVar(self) #Cree un StringVar vide

        try:
            self.varLigne2=StringVar(self, value=self.listAMod[1]) #Cree un StringVar contenant la seconde ligne
        except IndexError: #Si la ligne n'existe pas
            self.varLigne2=StringVar(self) #Cree un StringVar vide

        try:
            self.varLigne3=StringVar(self, value=self.listAMod[2]) #Cree un StringVar contenant la troisieme ligne
        except IndexError: #Si la ligne n'existe pas
            self.varLigne3=StringVar(self) #Cree un StringVar vide

        try:
            self.varLigne4=StringVar(self, value=self.listAMod[3]) #Cree un StringVar contenant la quatrieme ligne
        except IndexError: #Si la ligne n'existe pas
            self.varLigne4=StringVar(self) #Cree un StringVar vide

        try:
            self.varLigne5=StringVar(self, value=self.listAMod[4]) #Cree un StringVar contenant la cinquieme ligne
        except IndexError: #Si la ligne n'existe pas
            self.varLigne5=StringVar(self) #Cree un StringVar vide

        self.frameLignes=Frame(self)
        self.frameLignes.pack(side=TOP)

        self.varLigne1.trace('w',self.CallBack1) #En cas de modification
        self.ligne1=Entry(self.frameLignes,width=88,textvariable=self.varLigne1)
        self.ligne1.pack(side=TOP)

        self.varLigne2.trace('w',self.CallBack2) #En cas de modification
        self.ligne2=Entry(self.frameLignes,width=88,textvariable=self.varLigne2)
        self.ligne2.pack(side=TOP)

        self.varLigne3.trace('w',self.CallBack3) #En cas de modification
        self.ligne3=Entry(self.frameLignes,width=88,textvariable=self.varLigne3)
        self.ligne3.pack(side=TOP)

        self.varLigne4.trace('w',self.CallBack4) #En cas de modification
        self.ligne4=Entry(self.frameLignes,width=88,textvariable=self.varLigne4)
        self.ligne4.pack(side=TOP)

        self.varLigne5.trace('w',self.CallBack5) #En cas de modification
        self.ligne5=Entry(self.frameLignes,width=88,textvariable=self.varLigne5)
        self.ligne5.pack(side=TOP)

        self.frameBouton=Frame(self)
        self.frameBouton.pack(side=TOP)

        self.boutonEnre=Button(self.frameBouton,text="Enregistrer",command=self.Enregistrer)
        self.boutonEnre.pack(side=TOP)

        self.transient() #Declare fenetre secondaire
        self.grab_set()
        self.focus_set() #Focus de l'ecran
        self.wait_window() #Gele le reste du programe

    def Enregistrer(self):
        """Methode de la class FenModifHist
        Ajoute les lignes dans une list temporaire
        Puis utilise une fonction permettant de retirer les elements de la list a modif
        jusqua l'origine
        puis ajoute les lignes et ferme la fenetre
        """
        temp=[] #Liste temporaire
        if self.varLigne1.get()!="": #Si la list n'est pas vide
            temp.append(self.varLigne1.get()) #Ajoute la ligne

        if self.varLigne2.get()!="":
            temp.append(self.varLigne2.get())

        if self.varLigne3.get()!="":
            temp.append(self.varLigne3.get())

        if self.varLigne4.get()!="":
            temp.append(self.varLigne4.get())

        if self.varLigne5.get()!="":
            temp.append(self.varLigne5.get())

        listeElement=[]
        for element in self.listAMod: #Ajoute chaques elements dans une autre list temporaire
            listeElement.append(element)

        for element in listeElement: #Retire les elements de la list a modif a partire de la liste temporaire
            self.listAMod.remove(element)
        ##!!Raison: car si suppression direct d'un element dans une boucle for, saute des elements

        for element in temp: #Ajoute les elements de la list temporraire
            self.listAMod.append(element)

        self.destroy()

    def CallBack1(self,*arg):
        """Methode de la class FenModifHist
        CallBack de la ligne 1
        appele la methode CallBack en lui
        envoyant la variable de la ligne 1
        """
        self.CallBack(self.varLigne1)
    def CallBack2(self,*arg):
        """Methode de la class FenModifHist
        CallBack de la ligne 2
        appele la methode CallBack en lui
        envoyant la variable de la ligne 2
        """
        self.CallBack(self.varLigne2)
    def CallBack3(self,*arg):
        """Methode de la class FenModifHist
        CallBack de la ligne 3
        appele la methode CallBack en lui
        envoyant la variable de la ligne 3
        """
        self.CallBack(self.varLigne3)
    def CallBack4(self,*arg):
        """Methode de la class FenModifHist
        CallBack de la ligne 4
        appele la methode CallBack en lui
        envoyant la variable de la ligne 4
        """
        self.CallBack(self.varLigne4)
    def CallBack5(self,*arg):
        """Methode de la class FenModifHist
        CallBack de la ligne 5
        appele la methode CallBack en lui
        envoyant la variable de la ligne 5
        """
        self.CallBack(self.varLigne5)

    def CallBack(self, ligne, **arg):
        """Methode de la class FenModifHist
        demande une string var
        et empeche le depassement de 58 caracteres
        """
        if len(ligne.get())>58:
            temp=ligne.get()[:-1]
            ligne.set(temp)
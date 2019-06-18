#-------------------------------------------------------------------------------
# Name:        ModuleCarte
# Purpose:     Module de fonction/class concernant les cartes du logiciel Objectif_Terre
#
# Author:      Guillaume Lebegue
#
# Copyright:   (c) ikkino 2018
#-------------------------------------------------------------------------------

##Importation des modules necessaires-------------------------------------------
from tkinter import *
from tkinter.messagebox import *
import os
import pickle
from PIL import Image
from PIL import ImageTk

##Class-------------------------------------------------------------------------
class Map():
    """Class contenant la carte du jeu
    possede:
        -une hauteur
        -une longeur
        -une liste de rangee
        -un numero
        -un biome
        -des ressources
        -Une orientation(du joueur)
        -Une histoire
        -Le nombre d'action
    des fonctions:
        -CreeNouv
        -GenereRangee
        -Save
    """
    def __init__(self, mode=0, **kwargs):
        """Initialisateur"""
        self.h=0 #Hauteur
        self.l=0 #Longeur
        self.oriPers='N'#Orientation personage
        self.listerangee=[] #Liste de rangee
        self.num="" #Numero de la carte(le nom)
        self.sauvegarder=False #Si la carte a ete enregistrer
        self.biome="" #Le biome de la carte
        self.ressources="" #Les ressources de la carte
        self.chemin="" #Chemin d'enregistrement de la carte
        self.nbAvancer=-1
        self.nbTournerG=-1
        self.nbTournerD=-1
        self.nbTakeDrop=-1
        self.histPrec=[]
        self.histSuiv=[]
        self.mode=mode #Si une carte du joueur(1)

    def CreeNouv(self, parent):
        """Fonction de la class map
        Demande un widget parent
        Lance la creation d'une fenetre de selection
        Puis cree la nouvelle map"""
        FenetreNouv(self, parent) #Fenetre de selection
        if self.mode == 0:
            self.chemin = "Core/Map/"+self.num #Cree le chemin
        elif self.mode == 1:
            self.chemin = "Carte-Cree/"+self.num
        self.ressources = Ressources(self.biome) #Charge les ressources a partir du biome selectionner

        i=0
        while i<self.h: #Tant que i inferieur a la hauteur voulu
            self.GenereRangee() #Cree une rangee
            self.e=0
            while self.e<self.l-1: #Tant que e inferieur a la longeur voulu
                self.listerangee[i].GenereCase() #Cree une case dans la rangee
                self.e+=1
            i+=1

        self.sauvegarder=False #Sauvegarde reinitialiser

    def GenereRangee(self):
        """Fonction de la class map
        creant un objet de type rangee
        et l'ajoute a la liste de la carte
        """
        self.rangee=Rangee(self) #Cree un nouvel objet de type rangee
        self.listerangee.append(self.rangee) #L'ajoute a la liste

    def Save(self):
        """Fonction de la class map
        Enregistre la map
        Dans Core/Map
        Les ressources sont perdues dans le procede
        """
        if self.mode == 0:
            listeFichMap = os.listdir('Core/Map') #Liste de nom de fichier
        elif self.mode== 1:
            listeFichMap = os.listdir('Carte-Cree') #Liste de nom de fichier

        meme=False
        for Map in listeFichMap: #Pour chaque nom de map trouve
            if Map==self.num: #Si le nom donne est le meme
                meme=True

        if meme: #Si le nom donne est le meme
            if askyesno("Sauvegarder ?","Une carte a deja ete trouve, la remplacer ?"): #Fenetre oui/non du module tkinter.messageBox
                ressources=self.ressources #Enregistre les ressources dans une variable temporaire
                self.ressources="" #Reinitialise les ressources (On ne peut enregistrer des images)
                os.remove(self.chemin) #Supprime l'ancien fichier
                with open(self.chemin, 'wb') as fichier: #Utilisation du module pickle
                    pickler = pickle.Pickler(fichier)
                    pickler.dump(self) #Enregistrement
                self.ressources=ressources #Reafectation des ressources
                return 0
            else:
                return 1

        else: #Si le nom est different
            ressources=self.ressources #Enregistre les ressources dans une variable temporaire
            self.ressources="" #Reinitialise les ressources (On ne peut enregistrer des images)
            with open(self.chemin, 'wb') as fichier: #Utilisation du module pickle
                mon_pickler = pickle.Pickler(fichier)
                mon_pickler.dump(self) #Enregistrement
            self.ressources=ressources #Reafectation des ressources
            return 0


class Case():
    """Class d'objet creant des cases
    demande une rangee parent
    Possede:
        -Image
        -Rangee parent
        -Une action
        -Une liaison
    A pour variable de class:
        -compteur Compte le nombre de cases cree
        """
    def __init__(self, rangee,**kwargs):
        """Cree une case
        Demande la rangee parent
        """
        self.rangee=rangee #Rangee parent
        self.img=0 #Numero de l'image de la case
        self.liaison=''


class Rangee():
    """Class d'objet creant une rangee
    demande une map parent
    Possede:
        -Une map parent
        -Une liste de cases
    A pour fonctions:
        -GenereCase Cree une case dans la rangee
    """
    def __init__(self, map, **kwargs):
        """Cree une rangee
        et demande la creation d'une case
        Demande une map parent
        """
        self.map = map #map parent de la rangee
        self.listecase=[] #Liste de cases
        self.GenereCase() #Fonction

    def GenereCase(self):
        """Fonction de la class rangee
        cree un objet de type case
        """
        case=Case(self) #Cree une case
        self.listecase.append(case) #Ajoute la case a la liste de la rangee


class Ressources():
    """Class chargant les ressources d'un biome en particulier
    demande le type de biome
    Possede:
        -Un biome
        -Un chemin general
        -Beaucoup d'images
    """
    def __init__(self, biome, **kwargs):
        """Charge les ressources"""
        self.biome=biome #Biome
        self.cheminGen="Core/Ressources/{}/".format(self.biome) #Chemin general
        self.imgPerso=Image.open(self.cheminGen + "Perso.gif") #Image du perso de base
        self.imgPontF=Image.open(self.cheminGen + "pont_fermer.gif") #Image du pont fermer
        self.imgPontO=Image.open(self.cheminGen + "pont_ouvert.gif") #Image du pont ouvert
        self.imgBarriere=Image.open(self.cheminGen + "Barriere.gif")

        self.imgPontFN = ImageTk.PhotoImage(self.imgPontF) #Charge l'image
        self.imgPontON = ImageTk.PhotoImage(self.imgPontO) #Charge l'image
        self.imgPontFO = ImageTk.PhotoImage(self.imgPontF.rotate(90)) #Charge l'image
        self.imgPontOO = ImageTk.PhotoImage(self.imgPontO.rotate(90)) #Charge l'image
        self.imgBoutonJO = ImageTk.PhotoImage(file=self.cheminGen + "bouton_OFF.gif") #Charge l'image
        self.imgBoutonJF = ImageTk.PhotoImage(file=self.cheminGen + "bouton_ON.gif") #Charge l'image
        self.imgBoutonBO = ImageTk.PhotoImage(file=self.cheminGen + "Case_Bouton_Boite.gif") #Charge l'image
        self.imgStBoite = ImageTk.PhotoImage(file=self.cheminGen + "Case_Poser_Boite.gif") #Charge l'image
        self.img6 = ImageTk.PhotoImage(self.imgBarriere) #Charge l'image
        self.img7 = ImageTk.PhotoImage(self.imgBarriere.rotate(90)) #Charge l'image
        self.img8 = ImageTk.PhotoImage(file=self.cheminGen + "Croix_Barriere.gif") #Charge l'image
        self.imgVide = ImageTk.PhotoImage(file=self.cheminGen + "vide.gif") #Charge l'image
        self.imgSol = ImageTk.PhotoImage(file=self.cheminGen + "sol.gif") #Charge l'image
        self.imgStart = ImageTk.PhotoImage(file=self.cheminGen + "Start.gif") #Charge l'image
        self.imgEnd = ImageTk.PhotoImage(file=self.cheminGen + "End.gif") #Charge l'image
        self.imgPersoN = ImageTk.PhotoImage(self.imgPerso) #Image perso vers le nord
        self.imgPersoO = ImageTk.PhotoImage(self.imgPerso.rotate(90)) #Image perso vers l'ouest
        self.imgPersoE = ImageTk.PhotoImage(self.imgPerso.rotate(270)) #Image perso vers l'est
        self.imgPersoS = ImageTk.PhotoImage(self.imgPerso.rotate(180)) #Image perso vers le sud
        self.imgBoite = ImageTk.PhotoImage(file=self.cheminGen + "Boite.gif") #Charge l'image


class FenetreNouv(Toplevel): #Herite de Toplevel(Tkinter)
    """Fenetre secondaire permettant de rentrer
    les informations de la nouvelle carte
    possede:
        -une carte
        -une fenetre parent
        -l'orientation du perso
    Elements:
        -entry:
            -Numero
            -Longeur
            -Largeur
        -checkbox:
            -Orientation
        -listbox:
            -Biome
        -button:
            -Generer
    """
    def __init__(self, carte ,Master):
        """Demande une carte et un parent
        """
        Toplevel.__init__(self,Master) #Genere la fenetre secondaire

        self.carte=carte #Carte
        self.listeFichBiome = os.listdir('Core/Ressources') #Liste de nom de fichier
        self.listeFichBiome.remove('Core') #Retire Fichier non necessaires
        self.listeFichBiome.remove('Interface') #Retire Fichier non necessaires
        self.Orien='N' #Orientation par defaut

        ##Interface Toplevel----------------------------------------------------
        self.FrameNumero=Frame(self)
        self.FrameNumero.pack(fill=X,side=TOP)
        self.LabelNumero=Label(self.FrameNumero,text='Nom (max=10) :')
        self.LabelNumero.pack(side=LEFT)
        self.VarNumero=StringVar() #String variable
        self.VarNumero.trace("w",self.VerifNum) #En cas de modification de la variable, appeler
        self.Numero=Entry(self.FrameNumero,textvariable=self.VarNumero,relief='ridge',bd=5) #Lie au string variable
        self.Numero.pack(side=RIGHT)

        self.FrameLongeur=Frame(self)
        self.FrameLongeur.pack(fill=X,side=TOP)
        self.LabelLongeur=Label(self.FrameLongeur,text='Longueur (max:10):')
        self.LabelLongeur.pack(side=LEFT)
        self.VarLongeur=StringVar()
        self.VarLongeur.trace("w",self.VerifLongeur) #En cas de modification de la variable, appeler
        self.Longeur=Entry(self.FrameLongeur,textvariable=self.VarLongeur,relief='ridge',bd=5) #Lie au string variable
        self.Longeur.pack(side=RIGHT)


        self.FrameLargeur=Frame(self)
        self.FrameLargeur.pack(fill=X,side=TOP)
        self.LabelLargeur=Label(self.FrameLargeur,text='Largeur (max:10):')
        self.LabelLargeur.pack(side=LEFT)
        self.VarLargeur=StringVar()
        self.VarLargeur.trace("w",self.VerifLargeur) #En cas de modification de la variable, appeler
        self.Largeur=Entry(self.FrameLargeur,textvariable=self.VarLargeur,relief='ridge',bd=5) #Lie au string variable
        self.Largeur.pack(side=RIGHT)


        self.FrameOrien=Frame(self)
        self.FrameOrien.pack(fill=X,side=TOP)
        self.CheckOrienN=Checkbutton(self.FrameOrien, text='N', command=lambda : self.CheckBox('N'))
        self.CheckOrienN.pack(side=LEFT)
        self.CheckOrienN.select() #Selectione par defaut
        self.CheckOrienS=Checkbutton(self.FrameOrien, text='S', command=lambda : self.CheckBox('S'))
        self.CheckOrienS.pack(side=LEFT)
        self.CheckOrienO=Checkbutton(self.FrameOrien, text='O', command=lambda : self.CheckBox('O'))
        self.CheckOrienO.pack(side=LEFT)
        self.CheckOrienE=Checkbutton(self.FrameOrien, text='E', command=lambda : self.CheckBox('E'))
        self.CheckOrienE.pack(side=LEFT)

        self.FrameBiome=Frame(self)
        self.FrameBiome.pack(fill=X,side=TOP)
        self.ListeBiom=Listbox(self.FrameBiome)
        self.ListeBiom.pack()

        self.FrameBouton=Frame(self)
        self.FrameBouton.pack(fill=X,side=TOP)
        self.Bouton=Button(self.FrameBouton,text='Generation',command=self.Select)
        self.Bouton.pack()

        ##Remplissage ListBox---------------------------------------------------
        for biome in self.listeFichBiome: #Pour chaque biomes dans la liste
            self.ListeBiom.insert(END, biome) #Ajout a la boite de selection
        self.ListeBiom.selection_set( first = 0 ) #Selection par defaut

        ##Parametrage Toplevel--------------------------------------------------
        self.protocol("WM_DELETE_WINDOW", self.Select) #Fermeture de la fenetre = fonction Select
        self.transient() #Declare fenetre secondaire
        self.grab_set()
        self.focus_set() #Focus de l'ecran
        self.wait_window() #Gele le reste du programe

    def VerifLargeur(self,*arg):
        """Verifie le widget entry
        Empeche l'ecriture d'autre chose que des chiffres
        """
        Verif=self.VarLargeur.get() #Recupere la valeur
        Verif=Verif.replace(' ','') #Retire les espaces
        Verifier=list() #Cree une liste vide

        try: #Essaie
            for Num in Verif: #Pour chaque chiffre dans verif
                if Num in ('0','1','2','3','4','5','6','7','8','9'): #Si le num est un chiffre
                    Verifier.append(Num) #Ajout Du chiffre

        except IndexError: #Sauf si la variable est vide
            pass
        self.VarLargeur.set(''.join(Verifier)) #Ajout des chiffres trouve

    def VerifLongeur(self,*arg):
        """Verifie le widget entry
        Empeche l'ecriture d'autre chose que des chiffres
        """
        Verif=self.VarLongeur.get() #Recupere la valeur
        Verif=Verif.replace(' ','') #Retire les espaces
        Verifier=list() #Cree une liste vide

        try: #Essaie
            for Num in Verif: #Pour chaque chiffre dans verif
                if Num in ('0','1','2','3','4','5','6','7','8','9'): #Si le num est un chiffre
                    Verifier.append(Num) #Ajout Du chiffre

        except IndexError: #Sauf si la variable est vide
            pass
        self.VarLongeur.set(''.join(Verifier)) #Ajout des chiffres trouve

    def VerifNum(self,*arg):
        """Verifie le widget entry
        Empeche l'ecriture d'autre chose que des chiffres
        """
        Verif=self.VarNumero.get() #Recupere la valeur
        Verif=Verif.replace(' ','') #Retire les espaces
        Verifier=list() #Cree une liste vide
        for elem in Verif:
            Verifier.append(elem)
        if len(Verifier) >10:
            Verifier.pop()
        self.VarNumero.set(''.join(Verifier)) #Ajout des chiffres trouve

    def Select(self):
        """Fonction de la class FenetreNouv
        Recupere la selection et la remplace dans le parent
        """
        if self.VarNumero.get()=='' or self.VarLargeur.get()=='' or self.VarLongeur.get()=='' or self.ListeBiom.curselection() ==(): #Si une des variables sont vide
            showerror('Valeur manquante', 'Toutes les valeurs n\'ont pas ete saisies') #Fenetre d'erreur de Tkinter

        elif int(self.VarLargeur.get()) < 1 or int(self.VarLargeur.get()) >10 or int(self.VarLongeur.get()) <1 or int(self.VarLongeur.get()) >10: #Si les variables ne sont pas dans l'ecart demande
            showerror('Grandeur/Longeur',"La grandeur ou la longeur rentrer n'est pas valide (max:10)") #Fenetre d'erreur de Tkinter

        else: #Si tout est bon
            self.carte.num = self.VarNumero.get() #Modification
            self.carte.h = int(self.VarLargeur.get()) #Modification
            self.carte.l = int(self.VarLongeur.get()) #Modification
            self.carte.biome = self.ListeBiom.get(self.ListeBiom.curselection()) #Recupere la selection et la modifie sur le parent
            self.carte.oriPers=self.Orien #Modification
            self.destroy() #Ferme la fenetre

    def CheckBox(self, box):
        """Deselectione les autres checkbox
        """
        if box=='N': #Si box selectioner est N
            self.CheckOrienS.deselect() #Deselectione
            self.CheckOrienO.deselect() #Deselectione
            self.CheckOrienE.deselect() #Deselectione
            self.Orien='N' #Modifie
        elif box=='S': #Si box selectioner est S
            self.CheckOrienN.deselect() #Deselectione
            self.CheckOrienO.deselect() #Deselectione
            self.CheckOrienE.deselect() #Deselectione
            self.Orien='S' #Modifie
        elif box=='O': #Si box selectioner est O
            self.CheckOrienN.deselect() #Deselectione
            self.CheckOrienS.deselect() #Deselectione
            self.CheckOrienE.deselect() #Deselectione
            self.Orien='O' #Modifie
        elif box=='E': #Si box selectioner est E
            self.CheckOrienN.deselect() #Deselectione
            self.CheckOrienS.deselect() #Deselectione
            self.CheckOrienO.deselect() #Deselectione
            self.Orien='E' #Modifie

##Fonction----------------------------------------------------------------------
def Ouvrir(numero,mode=0):
    """Fonction du module ModuleCarte
    demande un numero(str)
    renvoi la map correspondante
    (sans ressources)
    Chemin: Core/Map/numero
    """
    if mode == 0:
        chemin = "Core/Map/"+numero #Cree le chemin
    elif mode == 1:
        chemin = "Carte-Cree/"+numero
    with open(chemin, 'rb') as fichier: #Utilisation du module pickle
        depickler = pickle.Unpickler(fichier)
        carte = depickler.load() #Chargement du fichier
    return carte #Renvoi la carte charge

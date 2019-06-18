#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ikkin
#
# Created:     18/05/2018
# Copyright:   (c) ikkin 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pickle

def main():
    pass

if __name__ == '__main__':
    main()
    with open("3", 'rb') as fichier: #Utilisation du module pickle
        depickler = pickle.Unpickler(fichier)
        nbDebloque = depickler.load() #Chargement du fichier
    print(nbDebloque)

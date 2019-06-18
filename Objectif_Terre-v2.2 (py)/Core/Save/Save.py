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
    nbDebloque="02"
    with open("3", 'wb') as fichier: #Utilisation du module pickle
        pickler = pickle.Pickler(fichier)
        pickler.dump(nbDebloque) #Enregistrement


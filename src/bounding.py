#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 21:12:23 2018

@author: cecilebecquie
"""
# Boîte qui prend le dessin
from numpy import asarray, zeros, uint8

import cv2
import __var__ as glb

def processing():
    img = cv2.imread(glb.cam) # Chargement de l'image
    col = asarray(glb.main_color)

    y, x, z = img.shape # Définition du x et du y (x = largeur / y = hauteur)
    xf, yf = [], [] # Tableau de tracking du rouge (pour l'instant)


    # Analyse de la couleur des pixels de l'image pixel par pixel
    # Analyse de la manière suivante :
    # Pour une hauteur fixe, analyse des pixels en largeur
    # ex: ligne 0 --> anlyse du pixel colonne 0 au pixel colonne 599
    # ex: ligne 1 --> anlyse du pixel colonne 0 au pixel colonne 599
    # ex: ligne 2 --> anlyse du pixel colonne 0 au pixel colonne 599
    # etc...
    for i in range (0, y):
        for j in range (0, x):
        
            # Détection de la couleur rouge seulement (à changer pour une autre couleur si possible)
            # AIDE:
            # 0 = bleu
            # 1 = vert
            # 2 = rouge
            if (img[i, j, 0] == col[0]) and (img[i, j, 1] == col[1]) and (img[i, j, 2] == col[2]):
                xf.append(j) # Insère la colonne du pixel rouge dans un tableau
                yf.append(i) # Insère la ligne du pixel rouge dans un tableau

    # Tri des valeurs min et max de chaque tableau
    
    # Pour le tableau des x :          
    # Définition des variables max/min
    min_xf = xf[0]
    max_xf = xf[0]
    
    # Cherche les plus petites et plus grandes valeurs des pixels en x
    for i in range (0, len(xf)):
        if min_xf > xf[i]:
            min_xf = xf[i]
        elif max_xf < xf[i]:
            max_xf = xf[i]
                
    # Pour le tableau des y :
    # Définition des variables max/min
    min_yf = yf[0]
    max_yf = yf[0]

    # Cherche les plus petites et plus grandes valeurs des pixels en y
    for i in range (0, len(yf)):
        if min_yf > yf[i]:
            min_yf = yf[i]
        elif max_yf < yf[i]:
            max_yf = yf[i]
 
    # Déssine un rectangle sur l'image
    # Le rectangle entoure exactement le tracé
    cv2.rectangle(img,(min_xf, min_yf),(max_xf, max_yf),(0,0,0),2)

    # Définition de la hauteur et de la largeur de l'image finale
    width = max_xf - min_xf
    height = max_yf - min_yf

    # Définition des variables
    blank_image = zeros((height,width,3), uint8) # Création d'une image vide
    k, l = 0, 0 # Définition des indices pour la copie des pixels

    # Copie des pixels dans le rectangle, pixel par pixel, sur une image vierge 
    for i in range (min_yf, max_yf):
        for j in range (min_xf, max_xf):
            blank_image[k, l, 0] = img[i, j, 0] # Copie des pixels bleu
            blank_image[k, l, 1] = img[i, j, 1] # Copie des pixels vert
            blank_image[k, l, 2] = img[i, j, 2] # Copie des pixels rouge
        
            l+=1 # Incrémentation de l'indice de la largeur
        
            # Réinitialisation de l'indice une fois la largeur max atteinte
            if l == width:
                l = 0
        k+=1 # Incrémentation de l'indice de la hauteur
    
        # Réinitialisation de l'indice une fois la hauteur max atteinte
        if k == height:
            k = 0

    cv2.imwrite(glb.saved, blank_image) # Enregistrement de l'image finale
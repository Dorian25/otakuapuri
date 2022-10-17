# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:16:36 2022

@author: Dorian
"""

class Serie:
    def __init__(self, serie_dict):
        self.annee_sortie = serie_dict["Année de Sortie"] if "Année de Sortie" in serie_dict else ""
        self.auteur = serie_dict["Auteur"] if "Auteur" in serie_dict else ""
        self.chapitres = serie_dict["Chapitres"] if "Chapitres" in serie_dict else ""
        self.dessinateur = serie_dict["Dessinateur"] if "Dessinateur" in serie_dict else ""
        self.statut = serie_dict["Statut"] if "Statut" in serie_dict else ""
        self.synopsis = serie_dict["Synopsis"] if "Synopsis" in serie_dict else ""
        self.titre = serie_dict["Titre"] if "Titre" in serie_dict else ""
        self.type_serie = serie_dict["Type"] if "Type" in serie_dict else ""
        self.volumes = serie_dict["Volumes"] if "Volumes" in serie_dict else ""
        
        
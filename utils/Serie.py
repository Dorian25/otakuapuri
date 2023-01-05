# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:16:36 2022

@author: Dorian
"""

class Serie:
    def __init__(self, serie_dict):
        self.annee_sortie = serie_dict["Année de Sortie"] if "Année de Sortie" in serie_dict else ""
        self.auteur = serie_dict["Auteur"] if "Auteur" in serie_dict else ""
        self.chapitres = {chapitre["Numéro"]: chapitre['Pages'] for chapitre in serie_dict["Chapitres"]}
        self.volumes_dict = {chapitre["Numéro"]: chapitre['Pages'] for chapitre in serie_dict["Chapitres"]}
        self.dessinateur = serie_dict["Dessinateur"] if "Dessinateur" in serie_dict else ""
        self.statut = serie_dict["Statut"] if "Statut" in serie_dict else ""
        self.synopsis = serie_dict["Synopsis"] if "Synopsis" in serie_dict else ""
        self.titre = serie_dict["Titre"] if "Titre" in serie_dict else ""
        self.type_serie = serie_dict["Type"] if "Type" in serie_dict else ""
        self.volumes = {volume["Numéro"]: volume['Pages'] for volume in serie_dict["Volumes"]}

    def get_list_numeros_chapitres(self):
        """Permet d'obtenir la liste de tous les numéros de chapitres de la série

        Returns:
            list[str]: liste des numéros de chapitres
        """
        return list(self.chapitres.keys())

    def get_list_numeros_volumes(self):
        """Permet d'obtenir la liste de tous les numéros de volumes de la série

        Returns:
            list[str]: liste de numéros de volumes
        """
        return list(self.volumes.keys())

    def get_number_volumes(self):
        """Retourne le nombre de volumes de la série

        Returns:
            int: nombre de volumes
        """
        return len(self.volumes)

    def get_covers_volumes(self):
        """Retourne une liste d'url vers la page de couverture (img) de chaque volume de la série

        Returns:
            list[str]: liste d'url  
        """
        return [volume["Pages"][0] for volume in self.volumes]

    def get_number_chapitres(self):
        """Retourne le nombre de chapitres de la série

        Returns:
            int: nombre de chapitres
        """
        return len(self.chapitres)
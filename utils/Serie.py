# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 17:16:36 2022

@author: Dorian
"""

from utils.utils import *
from utils.FileManager import DIR_TMP_CHARACTERS

class Serie(object):
    """Classe représentant une série
    """
    def __init__(self, serie_dict, mal_dict=None, anime_dict=None):
        self.titre = serie_dict["Titre"] if "Titre" in serie_dict else ""

        self.synopsis = serie_dict["Synopsis"] if "Synopsis" in serie_dict else ""
        
        self.statut = serie_dict["Statut"] if "Statut" in serie_dict else serie_dict["Status"] if "Status" in serie_dict else "Unknown"
        self.type = serie_dict["Type"] if "Type" in serie_dict else "Unknown"
        self.annee_sortie = serie_dict["Année de Sortie"] if "Année de Sortie" in serie_dict else "Unknown"
        self.auteur = serie_dict["Auteur"] if "Auteur" in serie_dict else "Unknown"
        self.dessinateur = serie_dict["Dessinateur"] if "Dessinateur" in serie_dict else "Unknown"

        self.volumes = {volume["Numéro"]: volume['Pages'] for volume in serie_dict["Volumes"]} if "Volumes" in serie_dict else {}
        self.chapitres = {chapitre["Numéro"]: chapitre['Pages'] if 'Pages' in chapitre else [] for chapitre in serie_dict["Chapitres"]} if "Chapitres" in serie_dict else {}

        self.cover = serie_dict["URL_COVER"] if "URL_COVER" in serie_dict else self.get_cover()
        
        # MAL Info
        self.statistics = mal_dict["Statistics"] if mal_dict else None
        self.rank = mal_dict["Rank"] if mal_dict else ""
        self.characters = mal_dict["Characters"] if mal_dict else []
        self.information = mal_dict["Information"] if mal_dict else None

        # Anime-Sama Info
        self.versions = anime_dict["Anime"] if anime_dict else {}
        self.seasons_vostfr = anime_dict["Anime"]["VOSTFR"] if self.versions and "VOSTFR" in self.versions else None
        self.seasons_vf = anime_dict["Anime"]["VF"] if self.versions and "VF" in self.versions else None

    def get_cover(self):
        if len(self.volumes)>0:
            return self.volumes["1"][0]                                   
        elif len(self.chapitres)>0 :
            return self.chapitres["1"][0]
        else :
            return ""
        
    def get_number_versions(self):
        return len(self.versions)

    def get_top20_characters(self):
        """_summary_

        Returns:
            dict: _description_
        """
        top20characters = sorted(self.characters, key= lambda d: d['n_favorites'], reverse=True)[:20]

        for rank, d in enumerate(top20characters):
            d.update({"path_image": DIR_TMP_CHARACTERS + 
                                    str(rank) + "_" +  
                                    d['name'].lower().replace(',','').replace('.','').replace(' ','_') + 
                                    getFormatImage(d['url_image'])})
                  
        return top20characters


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
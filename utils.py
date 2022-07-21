# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:35:02 2022

@author: Dorian
"""


import os

import img2pdf

from bs4 import BeautifulSoup
import cloudscraper
import urllib.request

import time
import random


#############################################################################
website_top_manga = "https://myanimelist.net/topmanga.php"

website_scan = {"sushi-scan" : "https://sushiscan.su/manga/list-mode/",
                "scan-manga" : "https://scan-manga.com"}

scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance

dict_mois = {"janvier" : "01",
             "février" : "02",
             "mars" : "03",
             "avril" : "04",
             "mai" : "05",
             "juin" : "06",
             "juillet" : "07",
             "août" : "08",
             "septembre" : "09",
             "octobre" : "10",
             "novembre" : "11",
             "décembre" : "12"}
#############################################################################
def test_internet(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

def format_date(t_d) :
    t_date = t_d.split(" ")
    new_date = "/".join([t_date[1].replace(",",""),dict_mois[t_date[0]],t_date[2]])
    return new_date

def format_txt_info(txt) :
    step1 = txt.replace("\n","")
    if step1.startswith("Statut ") :
        t = step1.split("Statut ")
        return 'Statut', t[1]
    elif step1.startswith("Type ") :
        t = step1.split("Type ")
        return 'Type', t[1]
    elif step1.startswith("Année de Sortie ") :
        t = step1.split("Année de Sortie ")
        return 'Année de Sortie', t[1]
    elif step1.startswith("Auteur ") :
        t = step1.split("Auteur ")
        return 'Auteur', t[1]
    elif step1.startswith("Dessinateur ") :
        t = step1.split("Dessinateur ")
        return 'Dessinateur', t[1]
    elif step1.startswith("Posté par ") :
        t = step1.split("Posté par ")
        return 'Posté par', t[1]
    elif step1.startswith("Prépublié dans ") :
        t = step1.split("Prépublié dans ")
        return 'Prépublié dans', t[1]
    elif step1.startswith("Posté le ") :
        t = step1.split("Posté le ")
        return 'Posté le', format_date(t[1])
    elif step1.startswith("Mis à jour le ") :
        t = step1.split("Mis à jour le ")
        return 'Mis à jour le', format_date(t[1])
    else :
        return False
    return step1

def get_all_mangas() :  
    html_website = BeautifulSoup(scraper.get(website_scan["sushi-scan"]).text, 'html.parser')
    
    div_list = html_website.find("div", {"class" : "soralist"})
    all_books = div_list.findAll("a", {"class" : "series"})
    all_books_txt = [(a.text, a["href"]) for a in all_books]
    
    return all_books_txt

def get_all_datas_of_manga(title_manga, url_manga):
    # data to get :
        # left info : statut, type, année de sortie, auteur, posté le, mis à jour le
        # right info : all volumes and all url, number of volume
        
    creators = []
    volumes = []
    
    html_website = BeautifulSoup(scraper.get(url_manga).text, 'html.parser')
        
    div_left_info = html_website.find("div", {"class" : "info-left"})
    div_right_info = html_website.find("div", {"class" : "info-right"})
        
    # left info
    div_tsinfo_bixbox = div_left_info.find("div", {"class" : "tsinfo bixbox"})
    all_div_info = div_tsinfo_bixbox.findAll("div", {"class" : "imptdt"})
        
    synopsis = div_right_info.find("div", {"class" : "entry-content entry-content-single"})
        
    row = {"Titre":title_manga,
           "Synopsis" : synopsis.text}
        
    for div_info in all_div_info :
        txt_info = div_info.text
        if format_txt_info(txt_info) :
            k,v = format_txt_info(txt_info)
            row[k] = v
           
    serie = (row["Titre"],
             row["Synopsis"],
             row["Type"],
             row["Année de Sortie"] if "Année de Sortie" in row else "None",
             row["Statut"])
        
       
    # right info
    div_chapterlist = div_right_info.find("div", {"id" : "chapterlist"})
    all_a_chapters = div_chapterlist.findAll("a")
    
    for a_chapter in all_a_chapters :
        volume_name = a_chapter.find("span",{"class" : "chapternum"}).text.strip()
        date_ajout = a_chapter.find("span", {"class" : "chapterdate"}).text
        
        t = a_chapter["href"].split("-")
        type_volume = t[-2].lower()
        numero = t[-1].replace("/","")
        print(type_volume, numero)
        volumes.append((volume_name,
                        numero,
                        type_volume,
                        format_date(date_ajout),
                        a_chapter["href"],
                        title_manga))
        
        
    creators.append((row["Auteur"] if "Auteur" in row else "", "auteur"))
    creators.append((row["Dessinateur"] if "Dessinateur" in row else "", "dessinateur"))
        
    return creators, serie, volumes

def getFormatFile(file):
    return file.split(".")[1]

def getNameFile(file):
    return file.split(".")[0]

def create_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("La création du dossier",path,"n'a pas pu aboutir. Il existe peut être déjà.")
    else:
        print ("Le dossier",path,"a été créé correctement")
        
def sortedFiles(l) :
    l.sort(key = lambda x: int(x.split(".")[0]))

    return l

def getFormatImage(image_url) :

    format_img = image_url.split("/")[-1].split(".")[-1]
    
    return "."+format_img

        
def convert_to_pdf(path_pdf_file, dir_tmp_pages="tmp/pages/"):
    
    sorted_pages = [os.path.join(dir_tmp_pages, name) for name in sortedFiles(os.listdir(dir_tmp_pages))]
    
    with open(path_pdf_file, "wb") as f :
        f.write(img2pdf.convert(sorted_pages))

    print(path_pdf_file,"généré")        
        
def get_cover_manga(title_manga, n_vol, url_manga, download_dir) :
    html_volume = BeautifulSoup(scraper.get(url_manga).text, 'html.parser')

    url_cover = html_volume.find("div",{"id":"readerarea"}).findAll("img")[0]
    

    clean_url_img = url_cover["src"]
    format_img = getFormatImage(clean_url_img)
                
    time.sleep(random.random())
    urllib.request.urlretrieve(clean_url_img, 
                               download_dir+"cover_"+title_manga+n_vol+format_img)
    
    return download_dir+"cover_"+title_manga+n_vol+format_img
    
def get_all_pages_url(url_volume,  ) :
    html_volume = BeautifulSoup(scraper.get(url_volume).text, 'html.parser')

    list_pages = html_volume.find("div",{"id":"readerarea"}).findAll("img")
    list_url = [img["src"] for img in list_pages]
    
    return list_url

def download_page(url_page, num_page, dir_tmp_pages="tmp/pages/") :
        
        format_img = getFormatImage(url_page)
                
        if not (os.path.exists(dir_tmp_pages+str(num_page+1)+format_img)) :
            time.sleep(random.random())
            urllib.request.urlretrieve(url_page, 
                                       dir_tmp_pages+str(num_page+1)+format_img)
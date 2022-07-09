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
#############################################################################

def format_date(t_d) :
    t_date = t_d.split(" ")
    new_date = t_date[1].replace(",","") + " " +  t_date[0] + " " + t_date[2]
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

def get_all_mangas_infos(list_mangas):
    
    # data to get :
        # left info : statut, type, année de sortie, auteur, posté le, mis à jour le
        # right info : all volumes and all url, number of volume
    
    data = []
    
    for title_manga, url_manga in list_mangas :
        html_website = BeautifulSoup(scraper.get(url_manga).text, 'html.parser')
        div_left_info = html_website.find("div", {"class" : "info-left"})
        #div_right_info = html_website.find("div", {"class" : "info-right"})
        div_tsinfo_bixbox = div_left_info.find("div", {"class" : "tsinfo bixbox"})
        all_div_info = div_tsinfo_bixbox.findAll("div", {"class" : "imptdt"})
        
        row = {"Titre":title_manga}
        
        for div_info in all_div_info :
            txt_info = div_info.text
            if format_txt_info(txt_info) :
                k,v = format_txt_info(txt_info)
                #v = div_info.find("i").text
                row[k] = v
           
        data.append((row["Titre"],
                     row["Statut"],
                     row["Type"],
                     row["Année de Sortie"] if "Année de Sortie" in row else "Unknown",
                     row["Auteur"] if "Auteur" in row else row["Dessinateur"],
                     row[""]))
        
    return data

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

def convert_to_pdf_1(nom_manga_ebook,folder):       
    
    volumes = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

    for tome in volumes:
        DIR = folder+"/"+tome

        pages = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
        imagelist = []
        
        sorted_pages = sortedFiles(pages)

        for p in sorted_pages:
            if getFormatFile(p) == "webp" :
                new_name = getNameFile(p)+".png"
                webp.dwebp(DIR+"/"+p, DIR+"/"+new_name,"-o") 
                
                image = Image.open(DIR+"/"+new_name)
                im = image.convert('RGB')
                imagelist.append(im)
                
                os.remove(DIR+"/"+p)
                
            else :
                image = Image.open(DIR+"/"+p)
                im = image.convert('RGB')
                imagelist.append(im)
        
        imagelist[0].save(folder+"/"+nom_manga_ebook+tome+".pdf",save_all=True, append_images=imagelist[1:])
        print(folder+"/"+nom_manga_ebook+tome+".pdf","généré")

def convert_to_pdf_2(nom_manga_ebook,folder):       
    
    volumes = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]

    for tome in volumes:
        DIR = folder+"/"+tome

        sorted_pages = [os.path.join(DIR, name) for name in sortedFiles(os.listdir(DIR))]

        
        with open(folder+"/"+nom_manga_ebook+tome+".pdf", "wb") as f :
            f.write(img2pdf.convert(sorted_pages))

        print(folder+"/"+nom_manga_ebook+tome+".pdf","généré")




def get_all_images() :
    #html_website = BeautifulSoup(requests.get(website_url + nom_manga).text,"lxml")
    html_website = BeautifulSoup(scraper.get(website_url + nom_manga).text, 'html.parser')
    div_url_tomes = html_website.findAll("div", {"class" : "eph-num"})
    url_tomes = [div.find("a") for div in div_url_tomes][1:]

    n_tomes = len(url_tomes)
    
    for num_tome, url_tome in enumerate(url_tomes) :
        #on commence par le dernier
        tome = "tome_" + str(n_tomes - num_tome)
        
        if not (os.path.exists(folder+"/"+tome)):
                            
            create_directory(folder+"/"+tome)
            
            time.sleep(random.randint(5,10))
            html_tome = BeautifulSoup(scraper.get(url_tome["href"]).text,"html.parser")
            url_pages = html_tome.find("div",{"id":"readerarea"}).findAll("img")
            
            for num_page, url_img_page in enumerate(url_pages) :
                clean_url_img = url_img_page["src"]
                format_img = getFormatImage(clean_url_img)
                
                if not (os.path.exists(folder+"/"+tome+"/"+str(num_page+1)+format_img)) :
                    time.sleep(random.random())
                    urllib.request.urlretrieve(clean_url_img, 
                                               folder+"/"+tome+"/"+str(num_page+1)+format_img)
                    print("tome",tome,"page",num_page+1,"download")
        else :
            print("Vous avez déjà téléchargé le",tome)
            n_img_in_folder = len([name for name in os.listdir(folder+"/"+tome) if os.path.isfile(os.path.join(folder+"/"+tome, name))])
            print("=>",n_img_in_folder), "images téléchargées..."
            
            time.sleep(random.randint(5,10))
            html_tome = BeautifulSoup(scraper.get(url_tome["href"]).text,"html.parser")
            url_pages = html_tome.find("div",{"id":"readerarea"}).findAll("img")
            n_pages = len(url_pages)
            print("=>", n_pages, "images à télécharger...")
            
            if n_pages != n_img_in_folder :
                
                for num_page, url_img_page in enumerate(url_pages) :
                    clean_url_img = url_img_page["src"]
                    format_img = getFormatImage(clean_url_img)
                    
                    if not (os.path.exists(folder+"/"+tome+"/"+str(num_page+1)+format_img)) :
                        print(clean_url_img)
                        time.sleep(random.random())
                        urllib.request.urlretrieve(clean_url_img, 
                                                   folder+"/"+tome+"/"+str(num_page+1)+format_img)
                        print("tome",tome,"page",num_page+1,"download")
            else :
                print("Toutes les pages du tome ont été téléchargées !")







    
#######
#website_url = "https://sushi-scan.su/manga/"
#folder = "./Chainsaw_Man"
#nom_manga = "chainsaw-man"
#nom_manga_ebook = "chainsaw_man_"
#folder = "./Tokyo_Ghoul"
#nom_manga_ebook = "tokyo_ghoul_" 

#folder = "./Monster"
#nom_manga = "monster-edition-deluxe"
#nom_manga_ebook = "monster_"

#folder = "./Tokyo_Ghoul"
#nom_manga = "tokyo-ghoul"
#nom_manga_ebook = "tokyo_ghoul_"
#######  



#get_all_images()
#convert_to_pdf_2(nom_manga_ebook, folder)    

    

    


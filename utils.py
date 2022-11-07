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
from datetime import datetime
import random
import pandas as pd

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

# source : https://fictionhorizon.com/best-anime-quotes/
quotes_anime = ["People’s lives don’t end when they die, it ends when they lose faith.\n\t- Itachi Uchiha (Naruto)",
                "If you don’t take risks, you can’t create a future!\n\t- Monkey D. Luffy (One Piece)",
                "If you don’t like your destiny, don’t accept it.\n\t- Naruto Uzumaki (Naruto)",
                "When you give up, that’s when the game ends.\n\t- Mitsuyoshi Anzai (Slam Dunk)",
                "All we can do is live until the day we die. Control what we can... and fly free.\n\t- Deneil Young (Space Brothers)",
                "Forgetting is like a wound. The wound may heal, but it has already left a scar.\n\t- Monkey D. Luffy (One Piece)",
                "It’s just pathetic to give up on something before you even give it a shot.\n\t- Reiko Mikami (Another)",
                "If you don’t share someone’s pain, you can never understand them.\n\t- Nagato (Naruto)",
                "Whatever you lose, you’ll find it again. But what you throw away you’ll never get back.\n\t- Himura Kenshin (Rurouni Kenshin)",
                "We don’t have to know what tomorrow holds! That’s why we can live for everything we’re worth today!\n\t- Natsu Dragneel (Fairy Tail)",
                "Why should I apologize for being a monster? Has anyone ever apologized for turning me into one?”\n\t- Juuzou Suzuya (Tokyo Ghoul)",
                "People become stronger because they have memories they can’t forget.\n\t- Tsunade (Naruto)",
                "I’ll leave tomorrow’s problems to tomorrow’s me.\n\t- Saitama (One-Punch Man)",
                "If you wanna make people dream, you’ve gotta start by believing in that dream yourself!\n\t- Seiya Kanie (Amagi Brilliant Park)",
                "Being lonely is more painful then getting hurt.\n\t- Monkey D. Luffy (One Piece)",
                "There’s no shame in falling down! True shame is to not stand up again!\n\t- Shintarō Midorima (Kuroko’s Basketball)",
                "Simplicity is the easiest path to true beauty.\n- Seishuu Handa (Barakamon)",
                "If you can’t do something, then don’t. Focus on what you can.\n\t- Shiroe (Log Horizon)",
                "You can die anytime, but living takes true courage.\n\t- Kenshin Himura",
                "Every journey begins with a single step. We just have to have patience.\n\t- Milly Thompson",
                "It doesn’t do any good to pretend you can’t see what’s going on.\n\t- Yuuya Mochizuki (Another)",
                "Being weak is nothing to be ashamed of… Staying weak is !!\n\t- Fuegoleon Vermillion (Black Clover)",
                "To act is not necessarily compassion. True compassion sometimes comes from inaction.\n\t- Hinata Miyake (A Place Further than the Universe)",
                "A dropout will beat a genius through hard work.\n\t- Rock Lee (Naruto)",
                "Reject common sense to make the impossible possible.\n\t- Simon (Tengen Toppa Gurren Lagann)",
                "Whatever you lose, you’ll find it again. But what you throw away you’ll never get back.\n\t- Kenshin Himura (Rurouni Kenshin: Meiji Kenkaku Romantan)",
                "If you really want to be strong… Stop caring about what your surrounding thinks of you!\n\t- Saitama (One Punch Man)",
                "Vision is not what your eyes see, but an image that your brain comprehends.\n\t- Touko Aozaki (The Garden of Sinners / Kara no Kyōkai)",
                "Sometimes, people are just mean. Don’t fight mean with mean. Hold your head high.\n\t- Hinata Miyake (A Place Further than the Universe)",
                "The ticket to the future is always open.\n\t- Vash The Stampede (Trigun)",
                "Hard work is worthless for those that don’t believe in themselves.\n\t- Naruto Uzumaki (Naruto)",
                "A place where someone still thinks about you is a place you can call home.\n\t- Jiraiya (Naruto)",
                "Life comes at a cost. Wouldn’t it be arrogant to die before you’ve repaid that debt?\n\t- Yuuji Kazami (The Fruit of Grisaia)",
                "You can die anytime, but living takes true courage.\n\t- Himura Kenshin (Rurouni Kenshin)",
                "Every journey begins with a single step. We just have to have patience.\n\t- Milly Thompson (Trigun)",
                "If you just submit yourself to fate, then that’s the end of it.\n\t- Keiichi Maebara (Higurashi: When They Cry)",
                "It is at the moment of death that humanity has value.\n\t- Archer (Fate Series)",
                "People, who can’t throw something important away, can never hope to change anything.\n\t- Armin Arlert (Attack on Titan)",
                "Whatever you do, enjoy it to the fullest. That is the secret of life.\n\t- Rider (Fate Zero)",
                "Power comes in response to a need, not a desire. You have to create that need.\n\t- Goku (Dragon Ball Z)",
                "There are no regrets. If one can be proud of one’s life, one should not wish for another chance.\n\t- Saber (Fate Stay Night)",
                "You can’t always hold on to the things that are important. By letting them go we gain something else.\n\t- Kunio Yaobi (Tamako Market)",
                "If you don’t like your destiny, don’t accept it. Instead, have the courage to change it the way you want it to be.\n\t- Naruto Uzumaki (Naruto)",
                "Don’t beg for things. Do it yourself, or else you won’t get anything.\n\t- Renton Thurston (Eureka Seven)",
                "I refuse to let my fear control me anymore.\n\t- Maka Albarn (Soul Eater)",
                "If you can’t find a reason to fight, then you shouldn’t be fighting.\n\t- Akame (Akame Ga Kill)",
                "You should never give up on life, no matter how you feel. No matter how badly you want to give up.\n\t- Canaan",
                "People who can’t throw something important away, can never hope to change anything.\n\t- Armin Arlelt (Attack on Titan)",
                "We can’t waste time worrying about the what if’s.\n\t- Ichigo Kurosaki (Bleach)",
                "Fools who don’t respect the past are likely to repeat it.\n\t- Nico Robin (One Piece)",
                "That’s why I can’t make a change. Everything I do is so… Half-assed.\n\t- Hiroshi Kido (Barakamon)",
                "Sometimes it’s necessary to do unnecessary things.\n\t- Kanade Jinguuji (Best Student Council)",
                "An excellent leader must be passionate because it’s their duty to keep everyone moving forward.\n\t- Nico Yazawa (Love Live)",
                "Protecting someone means giving them a place to belong. Giving them a place where they can be happy.\n\t- Princess Lenessia (Log Horizon)",
                "Thinking you’re no-good and worthless is the worst thing you can do\n\t- Nobito (Doraemon)",
                "Sometimes I do feel like I’m a failure. Like there’s no hope for me. But even so, I’m not gonna give up. Ever!\n\t- Izuku Midoriya (My Hero Academia)",
                "If you can’t do something, then don’t. Focus on what you can do.\n\t- Shiroe (Log Horizon)",
                "When you lose sight of your path, listen for the destination in your heart.\n\t- Allen Walker (D.Gray Man)",
                "The moment you think of giving up, think of the reason why you held on so long.\n\t- Natsu Dragneel (Fairy Tail)",
                "Don’t give up, there’s no shame in falling down! True shame is to not stand up again!\n\t- Shintaro Midorima (Kuroko No Basket)",
                "No matter how hard or impossible it is, never lose sight of your goal.\n\t- Monkey D Luffy (One Piece)",
                "Life is not a game of luck. If you wanna win, work hard.\n\t- Sora (No Game No Life)",]
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
            
def get_synonyms(url): 
    serie_html = BeautifulSoup(scraper.get(url).text, 'html.parser')
    
    """span_title_english = serie_html.find("span", {"class":"title-english"})
    
    if span_title_english:
        return span_title_english.text.strip()
    else :
        return ""
        
    """
    
    left_side_div = serie_html.find("div", {"class" : "leftside"})\
                              .findAll("div", {"class" : "spaceit_pad"})
                              
    for div in left_side_div :
        if div.text.startswith("French:"):
            return div.text.split(":")[1].strip()
        if div.text.startswith("Type:"):
            return ""
    print("end loop")                          
    return ""  
          
def extract_top100_allmanga():
    url = "https://myanimelist.net/topmanga.php"
    
    html_website_p1 = BeautifulSoup(scraper.get(url).text, 'html.parser')
    html_website_p2 = BeautifulSoup(scraper.get(url+"?limit=50").text, 'html.parser')
    
    # liste de <tr class="ranking-list"></tr>
    list_tr_p1 = html_website_p1.findAll("tr", {"class" : "ranking-list"})
    list_tr_p2 = html_website_p2.findAll("tr", {"class" : "ranking-list"}) 
        
    top_100 = []
        
    # each tr == a row
    for tr in list_tr_p1+list_tr_p2[:10] :
        # each td == a column
        rank = tr.find("td",{"class": "rank ac"}).text
        title = tr.find("h3",{"class":"manga_h3"}).text
        href = tr.find("h3", {"class" : "manga_h3"}).find("a")["href"]
        french_title = get_synonyms(href)
        #title_info = detail.find("div",{"class":"information di-ib mt4"}).text
        score = tr.find("td",{"class": "score ac fs14"}).text
            
        top_100.append((rank.replace("\n",""),
                        title if len(french_title) == 0 else french_title,
                        score.replace("\n","")))
    
    save_top100(top_100, "allmanga")    
    
    return top_100

def save_top100(top_100, category, dir_docs="docs/"):        
    date = datetime.now().strftime("%d_%m_%Y")
     
    df_top_100 = pd.DataFrame(top_100, columns =['Rank', 'Title', 'Score'])
    
    if category == "allmanga":
        df_top_100.to_csv(f"top100_allmanga-{date}.csv", index=False)    

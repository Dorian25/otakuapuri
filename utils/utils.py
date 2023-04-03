# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:35:02 2022

@author: Dorian
"""

import os

import img2pdf

import urllib.request
import requests
import cloudscraper
from bs4 import BeautifulSoup

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from datetime import datetime
import random
import pandas as pd
import re
from urllib.parse import unquote

#############################################################################
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
    """Test if there is internet connection

    Args:
        host (str, optional): Google url. Defaults to 'http://google.com'.

    Returns:
        bool: True is there is internet, False otherwise
    """
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

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
    """_summary_

    Args:
        l (list[str]): _description_

    Returns:
        list[str]: _description_
    """
    l.sort(key = lambda x: int(x.split(".")[0]))

    return l

def getFormatImage(image_url) :
    """Retourne le format de l'image à partir de son url web (.format) ex: ".jpg", ".png" ...

    Args:
        image_url (str): url de l'image
        ex: 
        - https://cdn.myanimelist.net/r/42x62/images/questionmark_23.gif?s=f7dcbc4a4603d18356d3dfef8abd655c
        - https://sushiscan.net/wp-content/uploads8/ValkyrieApocalypseTome1-020.jpg
    Returns:
        str: format de l'image (ex: ".jpg", ".png" ...)
    """

    format_img = image_url.split("/")[-1].split('?')[0].split(".")[-1]

    
    return "."+format_img

        
def convert_to_pdf(path_pdf_file, dir_tmp_pages="tmp/pages/"):
    sorted_pages = [os.path.join(dir_tmp_pages, name) for name in sortedFiles(os.listdir(dir_tmp_pages))]
    
    with open(path_pdf_file, "wb") as f :
        f.write(img2pdf.convert(sorted_pages))

    print(path_pdf_file,"généré")        


def download_element(url_page, filename, dir_tmp) :
    # cloudscraper method 
    format_img = getFormatImage(url_page)

    scraper = cloudscraper.create_scraper()
    
    response = scraper.get(url_page)

    if response.status_code == 200 :
        img_data = scraper.get(url_page).content
        with open(dir_tmp + filename + format_img, 'wb') as f:
            f.write(img_data)
        scraper.close()
   
        return "[" + str(response.status_code) + "] - " + "GOOD REQUEST", dir_tmp + filename + format_img
    else :
 
        return "[" + str(response.status_code) + "] - " + "BAD REQUEST", dir_tmp + filename + format_img

    # undetected_chromedriver method
    '''
    if not(os.path.exists(dir_tmp_pages + str(num_page+1) + ".jpg")) :
        chrome_opts = uc.ChromeOptions()
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--headless")
        driver = uc.Chrome(options=chrome_opts)
            
        driver.get(url_page)
        try :
            image_tag = driver.find_element(By.TAG_NAME, "img")
            image_tag.screenshot(filename=dir_tmp_pages + num_page + ".jpg")
        except NoSuchElementException:
            return "BAD"
        driver.close()
        driver.quit()
    
        return "OK - " +  dir_tmp_pages+str(num_page+1) + ".jpg"
    '''

def top_100_mal(which, page=1):
    url = "https://myanimelist.net/topmanga.php"

    if which == "All Manga":
        url += ""
        if page == 2:
            url += "?limit=50"
    elif which == "Top Manga":
        url += "?type=manga"
        if page == 2:
            url += "&limit=50"
    elif which == "Most Popular":
        url += "?type=bypopularity"
        if page == 2:
            url += "&limit=50"

    response = requests.get(url)
    html_raw = response.content

    html_bs = BeautifulSoup(html_raw, "lxml")

    list_tr = html_bs.find_all("tr", {"class":"ranking-list"})

    ranking_list = []

    for tr in list_tr:
        td_rank = tr.find("td", {"class":"rank ac"})
        rank = td_rank.text.replace("\n","") 
        
        td_title = tr.find("td", {"class":"title al va-t clearfix word-break"})
        h3_title = td_title.find("h3")
        #div_info = td_title.find("div", {"class":"information di-ib mt4"})
        #split_info = [info.strip() for info in div_info.text.split("\n")[1:-1]]

        td_score = tr.find("td", {"class":"score ac fs14"})
        score = td_score.text.replace("\n","") 

        ranking_list.append((rank, h3_title.text, score))

    return ranking_list

def _search_regex(pattern, string, name, flags=0, group=None):
    """
    Perform a regex search on the given string, using a single or a list of
    patterns returning the first matching group.
    In case of failure return a default value or raise a WARNING or a
    RegexNotFoundError, depending on fatal, specifying the field name.
    """
    
    mobj = re.search(pattern, string, flags)
    
    if mobj:
        if group is None:
            # return the first matching group
            return next(g for g in mobj.groups() if g is not None)
        else:
            return mobj.group(group)
    else:
        print('unable to extract %s' % name)
        return None
    
def extract_real_url(url):
    response = requests.get(url)
    html_raw = response.content.decode('utf-8')

    myvi_id = _search_regex(r'CreatePlayer\s*\(\s*[\"\'].*?\bv=([\da-zA-Z_\W]+)\)',
                            html_raw, 
                            'video id')
    
    temp1 = myvi_id.split(", ")
    temp2 = temp1[0].split("\\u0026")

    real_url = unquote(temp2[0])

    return real_url


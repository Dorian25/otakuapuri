# -*- coding: utf-8 -*-
"""
Created on Wed May 25 15:35:02 2022

@author: Dorian
"""

import os

import img2pdf

import urllib.request
import requests

import time
from datetime import datetime
import random
import pandas as pd

#############################################################################
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
        
def get_cover_manga(title_manga, n_vol, url_cover, download_dir) :  
    clean_url_img = url_cover
    format_img = getFormatImage(clean_url_img)
                
    time.sleep(random.random())
    
    headers= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'
    }

    response = requests.get(clean_url_img, headers=headers)
    print(response.content)

    #urllib.request.urlretrieve(clean_url_img + "?__cf_chl_tk=115703tQtTjtxHr6l6EpKhMdN4RheKj1biDqoDyd.H0-1672851608-0-gaNycGzNB2U", 
    #                           download_dir+"cover_"+title_manga+n_vol+format_img)
    


    return download_dir+"cover_"+title_manga+"_"+n_vol+format_img
    

def download_page(url_page, num_page, dir_tmp_pages="tmp/pages/") :
        
        format_img = getFormatImage(url_page)
                
        if not (os.path.exists(dir_tmp_pages+str(num_page+1)+format_img)) :
            time.sleep(random.random())
            urllib.request.urlretrieve(url_page, 
                                       dir_tmp_pages+str(num_page+1)+format_img)
             
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:54:46 2022

@author: Dorian
"""

import sqlite3
import json
import requests
from utils.Serie import Serie

class MongoDBManager:
    def __init__(self):
        self.url = "https://data.mongodb-api.com/app/data-pfthg/endpoint/data/v1/action/"
        self.API_KEY = 'o8pywKI0RGODzcJiMIG7gvKehnmjAo5zIlN6uJGSlVOiRddZfptPIYtjF0d6Ka8n'
        self.headers = {'Content-Type': 'application/json',
                        'Access-Control-Request-Headers': '*',
                        'api-key': self.API_KEY,
        }
    
    def get_serie_infos(self, titre_serie):
        action = "findOne"
        serie = None
        
        payload = json.dumps({"collection": "sushiscan",
                              "database": "getmanga_db",
                              "dataSource": "GetMangaCluster",
                              "filter": {"Titre": titre_serie},
                              "projection": {"_id": 0}
                              })


        try:
            response = requests.request("POST", self.url+action, headers=self.headers, data=payload)
            response_json = response.json()
            serie = Serie(response_json["document"])
        except Exception as e:
            print("erreur", e)
            return serie
        finally:
            return serie
            
        
    def get_all_series(self):
        action = "find"
        
        payload = json.dumps({
            "collection": "sushiscan",
            "database": "getmanga_db",
            "dataSource": "GetMangaCluster",
            "projection": {
                "_id": 0,
                "Titre": 1
            }
        })


        try:
            response = requests.request("POST", self.url+action, headers=self.headers, data=payload)
            json_response = response.json()
          
            return [doc["Titre"] for doc in json_response["documents"]]
        except:
            print("erreur")
            return []
                
###

class SQLiteManager():
    def __init__(self, db_name):
        try :
            self.connection = sqlite3.connect(db_name)
            print("Creation",db_name,"- OK")
            self.cursor = self.connection.cursor()
            print("Connection", db_name, "- OK")
        except sqlite3.Error as error:
            print("Error", "- init DbManager -", error)
            
    def commit(self):
        self.connection.commit()
        
    def insert_into_serie(self, serie):
        sql_insert_serie = '''
                           INSERT INTO serie(title, synopsis, type, year_of_creation, status)
                           VALUES (?,?,?,?,?)
                           '''
        self.cursor.execute(sql_insert_serie, serie)
                    
    def insert_into_creator (self, creators) :               
        sql_insert_creator = '''
                             INSERT INTO creator(name, occupation)
                             VALUES (?,?)
                             '''
        self.cursor.executemany(sql_insert_creator, creators)
    
    def insert_into_has_created(self, has_created):
        # insert serie & insert creator MUST BE COMMITED BEFORE this insert
        
                    
        sql_insert_has_created = '''
                                 INSERT INTO has_created(id_creator, id_serie)
                                 VALUES ((SELECT id FROM creator WHERE name=?),(SELECT id FROM serie WHERE title=?))
                                 '''
        self.cursor.executemany(sql_insert_has_created, has_created)
                    
    def insert_into_volume(self, volumes):               
        sql_insert_tome = ''' 
                          INSERT INTO volume(title, numero, type, date_added, url, id_serie)
                          VALUES (?,?,?,?,?,(SELECT id FROM serie WHERE title = ?))
                          '''
        self.cursor.executemany(sql_insert_tome, volumes)
     
        
    def is_empty_db(self):
        try :
            self.cursor.execute('SELECT count(name) FROM sqlite_master')
    
            if self.cursor.fetchone()[0] == 1 :
                return True
            else :
                return False
        except sqlite3.Error as error:
            print("Error", "- is_empty_db DbManager -", error)
            
    def get_serie_infos(self, serie):
        self.cursor.execute("SELECT * FROM serie WHERE title=?", (serie,))
        res = self.cursor.fetchone()
        
        infos = {"id":res[0],
                 "title":res[1],
                 "synopsis":res[2],
                 "type":res[3],
                 "year":res[4],
                 "status":res[5]}
        
        self.cursor.execute('''SELECT *
                               FROM has_created
                               ''')
        infos["creators"] =  self.cursor.fetchall()  
                               
        self.cursor.execute('''SELECT numero, url 
                               FROM volume
                               WHERE id_serie=? AND type="volume"
                               ORDER BY date_added DESC''',(infos["id"],))
                               
        infos["volumes"] = list(self.cursor.fetchall())
        
        return infos
            
    def search_serie(self, typed):
        self.cursor.execute("SELECT title FROM serie WHERE title LIKE ?", (typed+"%",))
        res = [r[0] for r in self.cursor.fetchall()]
        return res
    
    def create_virtual_tables(self):
        try:
            self.cursor.execute(''' CREATE VIRTUAL TABLE serie USING fts5(title)''')
        except sqlite3.Error as error:
            print("Error", "- create_virtual_tables DbManager -", error) 
        
    def create_tables(self):
        try :
            self.cursor.execute(''' CREATE TABLE serie (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title VARCHAR(100),
                                    synopsis TEXT,
                                    type VARCHAR(20),
                                    year_of_creation VARCHAR(4),
                                    status VARCHAR(10)) ''')
                          
            self.cursor.execute(''' CREATE TABLE creator (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name VARCHAR(100),
                                    occupation VARCHAR(20)) ''')
                          
            self.cursor.execute(''' CREATE TABLE has_created (
                                    id_creator INTEGER,
                                    id_serie INTEGER,
                                    PRIMARY KEY(id_creator, id_serie),
                                    FOREIGN KEY(id_creator) REFERENCES creator(id),
                                    FOREIGN KEY(id_serie) REFERENCES serie(id)) ''')
                          
            self.cursor.execute(''' CREATE TABLE volume (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title VARCHAR(50),
                                    numero VARCHAR(4),
                                    type VARCHAR(10),
                                    date_added TIMESTAMP,
                                    url TEXT,
                                    id_serie INTEGER,
                                    FOREIGN KEY(id_serie) REFERENCES serie(id)) ''')
            
            self.connection.commit()
        except sqlite3.Error as error:
            print("Error", "- create_tables DbManager -", error) 
    
    def count_series(self):
        try :
            self.cursor.execute('SELECT count(*) from serie')
            return int(self.cursor.fetchone()[0])
        except sqlite3.Error as error:
            print("Error","- count_serie DbManager -", error)
    
    def count_volumes(self):
        try :
            self.cursor.execute("SELECT count(*) from volume where type='volume'")
            return int(self.cursor.fetchone()[0])
        except sqlite3.Error as error:
            print("Error","- count_volumes DbManager -", error)
            
    def count_chapters(self):
        try :
            self.cursor.execute("SELECT count(*) from volume where type='chapter'")
            return int(self.cursor.fetchone()[0])
        except sqlite3.Error as error:
            print("Error","- count_chapters DbManager -", error)
    
    def close(self):
        try :
            self.cursor.close()
            self.connection.close()
        except sqlite3.Error as error:
            print("Error", "- close DbManager -", error)        
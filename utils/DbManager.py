# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 22:54:46 2022

@author: Dorian
"""

import sqlite3
import json
import requests
from utils.Serie import Serie
import os

class MongoDBManager(object):
    # https://stackoverflow.com/questions/30556857/creating-a-static-class-with-no-instances
    @staticmethod
    def search_in_mal(title_serie):
        url = "https://data.mongodb-api.com/app/data-pfthg/endpoint/data/v1/action/"
        headers = {'Content-Type': 'application/json',
                        'Access-Control-Request-Headers': '*',
                        'api-key': os.getenv('API_KEY'),
        }

        action = "aggregate"
        result = None
        
        payload = json.dumps({"collection": "mal",
                              "database": "getmanga_db",
                              "dataSource": "GetMangaCluster",
                              "pipeline": [
                                            {
                                                "$search": {
                                                    "index": "title",
                                                    "text": {
                                                        "query": title_serie,
                                                        "path": {
                                                            "wildcard": "*"
                                                            }
                                                    }
                                                }
                                            },
                                            {
                                                "$limit": 3
                                            }
                                            #,
                                            #{
                                            #    "$project": {
                                            #        "score": { "$meta": "searchScore" }
                                            #    }
                                            #}
                                ]
                              })


        try:
            response = requests.request("POST", url+action, headers=headers, data=payload)
            response_json = response.json()
            
            result = response_json['documents'][0] if len(response_json['documents']) > 0 else None
        except Exception as e:
            print("erreur", e)
            return result
        finally:
            return result

    @staticmethod
    def search_in_mal_pymongo(title_serie):
        url = "https://data.mongodb-api.com/app/data-pfthg/endpoint/data/v1/action/"
        headers = {'Content-Type': 'application/json',
                        'Access-Control-Request-Headers': '*',
                        'api-key': os.getenv('API_KEY'),
        }

        action = "aggregate"
        result = None
        
        payload = json.dumps({"collection": "mal",
                              "database": "getmanga_db",
                              "dataSource": "GetMangaCluster",
                              "pipeline": [
                                            {
                                                "$search": {
                                                    "index": "title",
                                                    "text": {
                                                        "query": title_serie,
                                                        "path": {
                                                            "wildcard": "*"
                                                            }
                                                    }
                                                }
                                            },
                                            {
                                                "$limit": 3
                                            }
                                            #,
                                            #{
                                            #    "$project": {
                                            #        "score": { "$meta": "searchScore" }
                                            #    }
                                            #}
                                ]
                              })


        try:
            response = requests.request("POST", url+action, headers=headers, data=payload)
            response_json = response.json()
            
            result = response_json['documents'][0] if len(response_json['documents']) > 0 else None
        except Exception as e:
            print("erreur", e)
            return result
        finally:
            return result
    @staticmethod
    def search_in_sushiscan(title_serie):
        url = "https://data.mongodb-api.com/app/data-pfthg/endpoint/data/v1/action/"
        headers = {'Content-Type': 'application/json',
                        'Access-Control-Request-Headers': '*',
                        'api-key': os.getenv('API_KEY'),
        }
        action = "findOne"
        result = None
        
        payload = json.dumps({"collection": "sushiscan",
                              "database": "getmanga_db",
                              "dataSource": "GetMangaCluster",
                              "pipeline": [
                                            {
                                                "$search": {
                                                    "index": "title",
                                                    "text": {
                                                        "query": title_serie,
                                                        "path": {
                                                            "wildcard": "*"
                                                            }
                                                    }
                                                }
                                            }
                                ]
                              })


        try:
            response = requests.request("POST", url+action, headers=headers, data=payload)
            response_json = response.json()
            
        except Exception as e:
            print("erreur", e)
            return response_json
        finally:
            return response_json

    @staticmethod
    def get_serie_infos(titre_serie, website):
        url = "https://data.mongodb-api.com/app/data-pfthg/endpoint/data/v1/action/"
        headers = {'Content-Type': 'application/json',
                        'Access-Control-Request-Headers': '*',
                        'api-key': os.getenv('API_KEY'),
        }
        action = "findOne"
        serie = None
        
        payload = json.dumps({"collection": website,
                              "database": "getmanga_db",
                              "dataSource": "GetMangaCluster",
                              "filter": {"Titre": titre_serie},
                              "projection": {"_id": 0}
                              })

        try:
            response = requests.request("POST", url+action, headers=headers, data=payload)
            response_json = response.json()
            print(titre_serie.split(" – ")[0])
            mal_info = MongoDBManager.search_in_mal(titre_serie.split(" – ")[0])
            serie = Serie(response_json["document"], mal_info)
        except Exception as e:
            print("erreur", e)
            return None
        finally:
            return serie
            
    @staticmethod   
    def get_all_series(website):
        url = "https://data.mongodb-api.com/app/data-pfthg/endpoint/data/v1/action/"
        headers = {'Content-Type': 'application/json',
                        'Access-Control-Request-Headers': '*',
                        'api-key': os.getenv('API_KEY'),
        }
        action = "find"
        
        payload = json.dumps({
            "collection": website,
            "database": "getmanga_db",
            "dataSource": "GetMangaCluster",
            "projection": {
                "_id": 0,
                "Titre": 1
            }
        })


        try:
            response = requests.request("POST", url+action, headers=headers, data=payload)
            json_response = response.json()
          
            return [doc["Titre"] for doc in json_response["documents"]]
        except:
            print("erreur")
            return []

    @staticmethod
    def get_all_series_pymongo(client, website):
        db = client["getmanga_db"]

        website_collection = db[website]
        response = website_collection.find({}, projection={"_id": 0, "Titre": 1})

        return [doc["Titre"] for doc in response]

    @staticmethod
    def get_serie_infos_pymongo(client, titre_serie, website):
        title_edit = titre_serie.split(" – ")[0]

        db = client["getmanga_db"]
        db_anime = client["anime_db"]

        website_collection = db[website]
        mal_collection = db["mal"]
        animesama_collection = db_anime["anime-sama"]
        
        response_website = website_collection.find_one({"Titre": titre_serie}, projection={"_id": 0})
        response_mal = mal_collection.aggregate(pipeline= [{
                                                    "$search": {
                                                        "index": "title",
                                                        "text": {
                                                            "query": title_edit,
                                                            "path": {
                                                                "wildcard": "*"
                                                                }
                                                        }
                                                    }
                                                },
                                                {
                                                    "$limit": 1
                                                }
                                            #,
                                            #{
                                            #    "$project": {
                                            #        "score": { "$meta": "searchScore" }
                                            #    }
                                            #}
                                                ])
        response_animesama = animesama_collection.aggregate(pipeline=[{
                                                    "$search": {
                                                        "index": "title_animesama",
                                                        "text": {
                                                            "query": title_edit,
                                                            "path": {
                                                                "wildcard": "*"
                                                                }
                                                        }
                                                    }
                                                },
                                                {
                                                    "$limit": 1
                                                }
                                            #,
                                            #{
                                            #    "$project": {
                                            #        "score": { "$meta": "searchScore" }
                                            #    }
                                            #}
                                                ])
        list_mal = list(response_mal)
        list_animesama = list(response_animesama)

        best_res_mal = list_mal[0] if len(list_mal)>0 else None
        best_res_animesama = list_animesama[0] if len(list_animesama)>0 else None

        serie = Serie(serie_dict=response_website, mal_dict=best_res_mal, anime_dict=best_res_animesama)

        return serie
                
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
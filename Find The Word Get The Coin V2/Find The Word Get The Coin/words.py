import random, os
import sqlite3 as sql

class db:
    def __init__(self):
        currentPath = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(currentPath, "DB", 'words.db')
        self.conn = sql.connect(path)
        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS words ( ID INTEGER PRIMARY KEY )""")

    def getRandomWordID(self):
        return random.choice( [data[0] for data in  self.conn.execute("SELECT * FROM words").fetchall() ] )

    def getWordData(self, wordID, JSON):
        try:
            return JSON["words"][str(wordID)]
        except:
            return None
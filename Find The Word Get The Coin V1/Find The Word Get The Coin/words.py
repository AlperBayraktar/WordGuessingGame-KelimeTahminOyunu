import random
import sqlite3 as sql
from sqlite3.dbapi2 import Cursor

class db:
    def __init__(self):
        self.conn = sql.connect('DB/words.db')
        
        self.conn.execute("""CREATE TABLE IF NOT EXISTS words (
            ID INTEGER PRIMARY KEY,
            word TEXT,
            description TEXT)""")

    def addWord(self, word, description):
        try:
            self.conn.execute("INSERT INTO words(word,description) VALUES(?,?)", (word, description) )
            self.conn.commit()

            return "Added the word to database successfully."
        except Exception as error:
            return f"There was an error while adding the word to database.\nError: {error}"
    
    def deleteWord(self, word):
        try:
            self.conn.execute(f"DELETE FROM words WHERE word='{word}' ")
            self.conn.commit()

            return "Deleted the word successfully."
        except Exception as error:
            return f"There was an during deleting the word.\nError: {error}"
    
    def get(self, word):
        try:
            return self.conn.execute(f"SELECT * FROM words WHERE word='{word}' ").fetchone()
        except Exception as error:
            return (None, error)

    def getRandomWord(self):
        return random.choice(  [x[1] for x in list(self.conn.execute("SELECT * FROM words")) ]  )
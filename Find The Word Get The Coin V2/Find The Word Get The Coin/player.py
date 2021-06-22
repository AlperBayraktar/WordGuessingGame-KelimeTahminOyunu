import os
import sqlite3 as sql

class db:
    def __init__(self):
        currentPath = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(currentPath, "DB", 'player.db')
        self.conn = sql.connect(path)

        try:
            self.conn.execute("""CREATE TABLE player (
                ID INTEGER PRIMARY KEY,
                level INTEGER,
                coins INTEGER,
                last_word TEXT,
                guessed_words TEXT,
                language TEXT)""")
            
            # if there is no error, that means table is created for first time. Insert a new player data if table is first time
            # eğer tablo ilk kez yaratılmışsa hata çıkmaz ve bu kod çalışır, tablo ilk kez yaratılmışsa sıfır bir oyuncu verisi tabloya eklenir
            self.conn.execute("""INSERT INTO player (level, coins, last_word, guessed_words, language)
            VALUES(?,?,?,?,?)""", (1, 50, "{}", '[]', "en") )
            self.conn.commit()
        except Exception as e:
            pass

    def get(self, columnName):
        try:
            return self.conn.execute(f"SELECT {columnName} FROM player WHERE ID=1 ").fetchone()
        except:
            return None

    def update(self,columnName, newValue):
        try:
            self.conn.execute(f"UPDATE player SET {columnName}='{newValue}' WHERE ID=1")
            self.conn.commit()
            return [True]
        except Exception as error:
            return [False, error]
    
    def resetData(self):
        try:
            self.conn.execute("DROP TABLE player")
            self.__init__()
            return [True]
        except Exception as error:
            return [False, error]
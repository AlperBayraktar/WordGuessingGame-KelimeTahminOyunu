import sqlite3 as sql

class db:
    def __init__(self):
        self.conn = sql.connect('DB/player.db')

        try:
            self.conn.execute("""CREATE TABLE player (
                ID INTEGER PRIMARY KEY,
                level INTEGER,
                coins INTEGER,
                last_word TEXT,
                guessed_words TEXT)""")
            
            # if player table is created for the first time, this line will work and we will insert a row to table which contains the default data of player
            # eğer tablo ilk kez yaratılmışsa tabloya oyuncu için sıfır bir veri içeren bir satır ekleyeceğiz
            self.conn.execute("""INSERT INTO player(level, coins, last_word, guessed_words)
            VALUES(?,?,?,?)""", (1, 50, '', '[]') )
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
            return "SUCCESS"
        except:
            return "ERROR"
    
    def resetData(self):
        self.conn.execute("DROP TABLE player")
        self.__init__()
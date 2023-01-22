import psycopg2
from dbConnectionInfo import DB_NAME, DB_PASSWORD, DB_USER

class db:
    def __init__(self):
        # Connect
        self.conn = psycopg2.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}")
        self.cur = self.conn.cursor()

        # Create table if not exists
        self.cur.execute("""CREATE TABLE IF NOT EXISTS player (
            username VARCHAR(16), 
            coins INTEGER,
            hints_used INTEGER,
            language VARCHAR(5),
            last_word_id INTEGER,
            guessed_words_indexes INTEGER ARRAY)
            """)
        self.conn.commit()
        
        # Control if there is a user data
        # If there isn't, create a defaut player in db
        self.cur.execute("SELECT * FROM player")
        if self.cur.fetchone() == None:
            self.reset_data()

    def reset_data(self):
        self.cur.execute("DELETE FROM player")
        self.cur.execute("INSERT INTO player VALUES ('player', 60, 0, 'en', -1, '{}' )")
        self.conn.commit()

    def update(self, field, new_value):
        self.cur.execute(f"UPDATE player SET {field}={new_value}")
        self.conn.commit()
    
    def get(self, field):
        self.cur.execute(f"SELECT {field} FROM player")
        return self.cur.fetchone()[0]
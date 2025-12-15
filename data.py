import sqlite3
from pathlib import Path 


class ActivityDB:
    def __init__(self, db_name="activity.db"):

        # Vefitying the /data folder exists
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)

        # Path to data
        self.db_path = data_dir / db_name
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

        # Create the table if it doesn't exist
        #boolean is not a legit SQLite data type. Using it here for readability or in case of a future transition to something else.
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                date TEXT PRIMARY KEY,
                sleep BOOLEAN,
                resistance BOOLEAN,
                steps INTEGER,
                sauna BOOLEAN,
                cold_plunge BOOLEAN,
                sprint BOOLEAN,
                zone2cardio INTEGER,
                meditation INTEGER,
                core BOOLEAN,
                mobility BOOLEAN                           
                )
                """)
        self.conn.commit()


"""
import sqlite3
from pathlib import Path

class HealthDB:
    def __init__(self, db_path="health.db"):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                date TEXT PRIMARY KEY,
                steps INTEGER,
                sleep_hours REAL,
                calories INTEGER,
                mood TEXT,
                notes TEXT
            )
        """)
        self.conn.commit()

    def save_day(self, date, steps, sleep_hours, calories, mood, notes=""):
        self.cur.execute("""
            REPLACE INTO daily_metrics (date, steps, sleep_hours, calories, mood, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, steps, sleep_hours, calories, mood, notes))
        self.conn.commit()

    def get_day(self, date):
        self.cur.execute("SELECT * FROM daily_metrics WHERE date=?", (date,))
        return self.cur.fetchone()

    def get_all(self):
        self.cur.execute("SELECT * FROM daily_metrics ORDER BY date")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
        """
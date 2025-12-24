import sqlite3
from pathlib import Path 
from models.ActivityRow import ActivityRow

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
        # Daily Activiites Table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Activities (
                date_val TEXT PRIMARY KEY,
                sleep TEXT,
                resistance BOOLEAN,
                steps INTEGER,
                sauna BOOLEAN,
                cold_plunge BOOLEAN,
                sprint BOOLEAN,
                zone2cardio INTEGER,
                meditation INTEGER,
                hiit INTEGER,
                mobility BOOLEAN                           
                )
                """)
        
        # Metric Types Table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS MetricTypes (
                id INTEGER PRIMARY KEY,
                name TEXT,
                unit TEXT       
                )                     
             """)

        # Performance Metrics Trable
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS PerformanceMetrics(
                id INTEGER PRIMARY KEY,
                date_val TEXT,
                value REAL         
                )
                """)
        
        #User Data
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS UserData(
                name TEXT,
                level INTEGER             
                )
                """)
        
        #Attributes
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Attributes(
                attrib_number INTEGER PRIMARY KEY,
                name TEXT UNIQUE      
                )
                """)
        """Metric_based: Strength, Endurance, Agility
           Behavior_based: Disciplinie, Focus
           Hybrid: Constitution, Vitality, Dexterity"""

        self.conn.commit()

         #Levels
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Levels(
                level_number INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                point_threshold INTEGER
                )
                """)
        """0. Unready / Unlearned 0
           1. Initiate 100
           2. Disciple 500
           3. Strider 1500
           4. Adept 5000
           5. Guardian 10000
           6. Ascetic 25000
           7. Sentinel 40000
           8. Master 60000
           9. Vanguard 90000
           10. Vanguard Prime 200000"""

        self.conn.commit()
    def insert_activity(self, activity: ActivityRow):
        self.cur.execute(f"""
            INSERT INTO Activities ({", ".join(ActivityRow.columns())})
            VALUES ({", ".join(["?"] * len(ActivityRow.columns()))})
        """, activity.to_tuple())

        self.conn.commit()
    def get_activity(self, date_val):
        self.cur.execute("SELECT * FROM Activities WHERE date_val = ?", (date_val,))
        row = self.cur.fetchone()
        return ActivityRow.from_sqlite_row(row)
    
    def seed_standard_tables(self):
        """Populate tables like Levels if they are empty."""

        # Seed Levels table
        levels = [
            (0, "Unready", 0),
            (1, "Initiate", 100),
            (2, "Disciple", 500),
            (3, "Strider", 1500),
            (4, "Adept", 5000),
            (5, "Guardian", 10000),
            (6, "Ascetic", 25000),
            (7, "Sentinel", 40000),
            (8, "Master", 60000),
            (9, "Vanguard", 90000),
            (10, "Vanguard Prime", 200000),
        ]

        # Check if table already has data
        self.cur.execute("SELECT COUNT(*) FROM Levels")
        count = self.cur.fetchone()[0]

        if count == 0:
            self.cur.executemany(
                "INSERT INTO Levels (level_number, name, point_threshold) VALUES (?, ?, ?)",
                levels
            )
            self.conn.commit()
            print("Levels table populated.")
        else:
            print("Levels table already populated.")

def close(self):
    self.conn.close()

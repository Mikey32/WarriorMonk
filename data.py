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
        # Daily Activiites Table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                date TEXT PRIMARY KEY,
                sleep TEXT,
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
                date TEXT,
                value REAL         
                )
                """)
        
        #User Data
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS UserData(
                name TEXT             
                )
                """)
        
        #Attributes
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Atributes(
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
            CREATE TABLE IF NOT EXISTS Atributes(
                level_number INTEGER PRIMARY KEY,
                name TEXT UNIQUE            
                )
                """)
        """1. Initiate
           2. Disciple
           3. Strider
           4. Adept
           5. Guardian
           6. Ascetic
           7. Sentinel
           8. Master
           9. Vanguard
           10. Vanguard Prime"""

        self.conn.commit()

def close(self):
    self.conn.close()
"""
import sqlite3
from pathlib import Path

class HealthDB:


   

    def get_day(self, date):
        self.cur.execute("SELECT * FROM daily_metrics WHERE date=?", (date,))
        return self.cur.fetchone()

    def get_all(self):
        self.cur.execute("SELECT * FROM daily_metrics ORDER BY date")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
        """
from data import ActivityDB
from datetime import date
from modify_tasks import *
from models.ActivityRow import ActivityRow
import sys



def have(condition):
    if condition:
        return "have"
    else:
        return "have not"

def greet_user(activity, today):
    print("Good Morning " + str(activity.name) + ". Today is " + str(today))
    print("1. Last nights sleep was " + activity.sleep)
    print("2. Today you have  " + have(activity.resistance) + " resistance training")
    print("3. You have walked "+ str(activity.steps) +" steps.")
    print("3. You have "+ have(activity.sauna) + " sauna.")
    print("4. You have " + have(activity.cold_plunge) + " cold plunged.")
    print("5. You have " + have(activity.sprint) + " sprinted")
    print("6. You have done " + str(activity.zone2cardio) + " minutes of zone 2 cardio.")
    print("7. You meditated for "+ str(activity.meditation) +" minutes.")
    print("8. You have " + have(activity.core) + "core work.")
    print("9. You have " + have(activity.mobility) + "mobility work.")
    print("0. You can exit gracefully")


def main():
    db = ActivityDB()
    #Check if this is the first time running the program? If it is we need to set up the user database.
    db.cur.execute("SELECT COUNT(*) from UserData")
    count = db.cur.fetchone()[0]

    if count < 1:
        name = input("Welcome to the beginning of your journey of becoming a world class Warrior / Monk. Please enter what you would like to be called: ")
        db.cur.execute("INSERT INTO UserData (name) VALUES (?)", (name,))
        db.conn.commit()
    else:
        name = db.cur.execute("SELECT name from UserData WHERE 1=1")


    #Display current date and what has been accomplished.
    #Set values
    today = date.today().isoformat()
    
    default_values = {
    "date_val": today,
    "sleep": "Unknown",
    "resistance": False,
    "steps": 0,
    "sauna": False,
    "cold_plunge": False,
    "sprint": False,
    "zone2cardio": 0,
    "meditation": 0,
    "core": False,
    "mobility": False
    }   

    
    # Check if today's date exists in the database:
    db.cur.execute("SELECT * FROM activities WHERE date = ?", (today,))
    row = db.cur.fetchone()

    activity = ActivityRow.from_sqlite_row(row, default_values)
    

    userNumber = input(greet_user(activity, today))
    """
    print("Good Morning " + str(name) + ". Today is " + str(today))
    print("1. Last nights sleep was " + sleep)
    print("2. Today you have  " + have(resistance) + " resistance training")
    print("3. You have walked "+ str(steps) +" steps.")
    print("3. You have "+ have(sauna) + " sauna.")
    print("4. You have " + have(cold_plunge) + " cold plunged.")
    print("5. You have " + have(sprint) + " sprinted")
    print("6. You have done " + str(zone2cardio) + " minutes of zone 2 cardio.")
    print("7. You meditated for "+ str(meditation) +" minutes.")
    print("8. You have " + have(core) + "core work.")
    print("9. You have " + have(mobility) + "mobility work.")
    print("0. You can exit gracefully")
    """
   # userNumber = input()
    
    while userNumber > 0:
        match userNumber:
            case "1":
                modify_sleep(today)
            case "2":
                modify_resistance(today)
            case "3":
                modify_steps(today)
    print("Closing...")
    db.close()
    sys.exit(0)
    




if __name__ == "__main__":
    main()

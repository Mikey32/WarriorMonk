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
    

def greet_user(activity):
    print("1. Last nights' sleep was " + str(activity.sleep))
    print("2. Today you " + have(activity.resistance) + " done resistance training.")
    print("3. You have walked "+ str(activity.steps) +" steps.")
    print("4. You "+ have(activity.sauna) + " done sauna.")
    print("5. You " + have(activity.cold_plunge) + " cold plunged.")
    print("6. You " + have(activity.sprint) + " sprinted")
    print("7. You have done " + str(activity.zone2cardio) + " minutes of zone 2 cardio.")
    print("8. You meditated for "+ str(activity.meditation) +" minutes.")
    print("9. You have performed " + str(activity.hiit) + " minutes of a HIIT workout.")
    print("10. You " + have(activity.mobility) + " done mobility work.")
    print("0. You can exit gracefully.")
    userInput = input("Please enter your choice: ")
    return userInput


def main():
    
    #Check if this is the first time running the program? If it is we need to set up the user database.
    db.cur.execute("SELECT COUNT(*) from UserData")
    count = db.cur.fetchone()[0]

    if count < 1:
        name = input("Welcome to the beginning of your journey of becoming a world class Warrior / Monk. Please enter what you would like to be called: ")
        db.cur.execute("INSERT INTO UserData (name) VALUES (?)", (name,))
        db.conn.commit()
    else:
        db.cur.execute("SELECT name from UserData WHERE 1=1")
        name = db.cur.fetchone()[0]

    #Display current date and what has been accomplished.
    #Set values
    today = date.today().isoformat()
    
    default_values = {
    "date_val": today,
    "sleep": "unknown",
    "resistance": False,
    "steps": 0,
    "sauna": False,
    "cold_plunge": False,
    "sprint": False,
    "zone2cardio": 0,
    "meditation": 0,
    "hiit": 0,
    "mobility": False
    }   

    
    # Check if today's date exists in the database:
    db.cur.execute("SELECT * FROM Activities WHERE date_val = ?", (today,))
    row = db.cur.fetchone()

    if row is None:
        activity = ActivityRow.from_sqlite_row(row, default_values)
        db.insert_activity(activity)
    else:
        activity = ActivityRow.from_sqlite_row(row, default_values)

    print("Good Morning " + str(name) + ". Today is " + str(today))    

    userNumber = greet_user(activity)
    
    
    while int(userNumber) > 0:
        modify_activity(userNumber, today)
        activity = db.get_activity(today)
        userNumber = greet_user(activity)
       #userNumber = input(greet_user(activity))
        
    print("Closing...")
    sys.exit(0)
    db.close()
    
    


if __name__ == "__main__":
    db = ActivityDB()
    main()

from data import ActivityDB
from datetime import date
from modify_tasks import *
from models.ActivityRow import ActivityRow
from models.UserData import UserData
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", action="store_true", help="Populate standard tables")
    return parser.parse_args()

def have(condition):
    if condition:
        return "have"
    else:
        return "have not"
    
def greet_user(activity):
    print("0. You can exit gracefully.")
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
    print("11. Change day.")
    userInput = input("Please enter your choice: ")
    return userInput

def display_level(userData):
    updated_user, rank_title = check_for_promotion(userData)
    print(f"You are level {updated_user.level}. Youre rank is {rank_title}.")

def check_for_promotion(userData):
    #Check level based on xp?
    db.cur.execute("""
                    SELECT level_number, name
                    FROM Levels
                    WHERE point_threshold <= (
                        SELECT experience FROM UserData
                        )
                        ORDER BY point_threshold DESC
                        LIMIT 1;
                        """)
    level_number, rank_title = db.cur.fetchone()
    if level_number > userData.level:
        print(f"Congratulations {userData.name}! Welcome to level {level_number}. Your rank is {rank_title}.")
        db.cur.execute("""
                       UPDATE UserData
                       SET level = ?
                       """, (level_number,))
        db.conn.commit()
        db.cur.execute("SELECT name, level, experience FROM UserData LIMIT 1")
        userRow = db.cur.fetchone()
        userData = UserData.from_sqlite_row(userRow)
    return userData, rank_title



def main():
    
    #Check if this is the first time running the program? If it is we need to set up the user database.
    db.cur.execute("SELECT COUNT(*) from UserData")
    count = db.cur.fetchone()[0]
    

    if count < 1:
        name = input("Welcome to the beginning of your journey of becoming a world class Warrior / Monk. Please enter what you would like to be called: ")
        db.cur.execute("INSERT INTO UserData (name) VALUES (?)", (name,))
        db.conn.commit()
    else:

        db.cur.execute("SELECT name, level, experience FROM UserData LIMIT 1")
        userRow = db.cur.fetchone()
        userData = UserData.from_sqlite_row(userRow)
        name = UserData.name

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

    print("Good Day " + str(name) + ". Today is " + str(today))
   
    display_level(userData)    

    userNumber = greet_user(activity)
    check_weekly = False
        
    while int(userNumber) > 0:
        value = modify_activity(userNumber, today, check_weekly)
        if value == 11:
            today = input("Please enter the new day YYYY-MM-DD: ")
            check_weekly = True
        activity = db.get_activity(today)
        userNumber = greet_user(activity)

    print("Closing...")
    sys.exit(0)
    db.close()  

if __name__ == "__main__":
    db = ActivityDB()
    args = parse_args()

    if args.seed:
        db.seed_standard_tables()
        print("Database seeded.")
        exit(0)

    # Normal app flow continues here

    main()

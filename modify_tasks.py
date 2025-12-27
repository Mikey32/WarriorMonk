from data import ActivityDB
from datetime import date, timedelta

db = ActivityDB()

def modify_activity(taskNum, curdate, check_weekly):

    if check_weekly:
        WeeklyBonus.flag_week_for_recalc(curdate)

    match taskNum:
            case "1":
                modify_sleep(curdate)
            case "2":
                modify_resistance(curdate)
            case "3":
                modify_steps(curdate)
            case "4":
                modifiy_sauna(curdate)
            case "5":
                modify_cold_plunge(curdate)
            case "6":
                modify_sprint(curdate)
            case "7":
                modify_zone2(curdate)
            case "8":
                modify_meditation(curdate)
            case "9":
                modify_hiit(curdate)
            case "10":
                modify_mobility(curdate)
            case "11":
                return 11
    return

def modify_sleep(curdate):
    answer = input("How was your sleep?(y = good, n = not good)")
    #print(curdate)
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET sleep = ? WHERE date_val = ?",("good", curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE Activities SET sleep = ? WHERE date_val = ?",("not good", curdate))
    else:
        print("Invalid entry")
        return
    db.conn.commit()
    print("Sleep Updated!")
    return

def modify_resistance(curdate):
    answer = input("Did you do resistance?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET resistance = ? WHERE date_val = ?",(True, curdate))
        add_daily_xp()
    elif answer == 'n':
        #ToDo: Check if this was a y before, if so, remove daily XP.
        db.cur.execute("UPDATE Activities SET resistance = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    db.conn.commit()
    print("Resistance Updated!")
    return "Resistance Updated!"

def modify_steps(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many steps did you do?")
    db.cur.execute("UPDATE Activities SET steps = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    return "Steps Updated!"

def modifiy_sauna(curdate):
    answer = input("Did you use the sauna today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET sauna = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE Activities SET sauna = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    db.conn.commit()
    return "Sauna Updated!"

def modify_cold_plunge(curdate):
    answer = input("Did you cold plunge today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET cold_plunge = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE Activities SET cold_plunge = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    db.conn.commit()
    print("Cold Plunge Updated!")

def modify_sprint(curdate):
    answer = input("Did you sprint today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET sprint = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE Activities SET sprint = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    db.conn.commit()
    return "Sprint Updated!"

def modify_zone2(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many minutes of Zone 2 Cardio did you do?")
    db.cur.execute("UPDATE Activities SET zone2cardio = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    return "Zone 2 Cardio Updated!"

def modify_meditation(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many minutes of meditation did you do?")
    db.cur.execute("UPDATE Activities SET meditation = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    return "Meditation Updated!"

def modify_hiit(curdate):
    answer = input("How many minutes of high intensity interval training did you do today?")
    db.cur.execute("UPDATE Activities SET hiit = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    return "HIIT Updated!"

def modify_mobility(curdate):
    answer = input("Did you do mobility work today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET mobility = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE Activities SET mobility = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    db.conn.commit()
    return "Mobility Updated!"

 #Experience Gains
def add_daily_xp():
    db.cur.execute("UPDATE UserData SET experience = experience + 5")
    db.conn.commit()
def add_weekly_task_xp():
    db.cur.execute("UPDATE UserData SET experience = experience + 10")
    db.conn.commit()

 #Experience losses (currently only if a mistake was made and something done is now undone):
def remove_daily_xp():
    db.cur.execute("UPDATE UserData SET experience = experience - 5")
    db.conn.commit()
def remove_weekly_task_xp():
    db.cur.execute("UPDATE UserData SET experience = experience - 10")
    db.conn.commit()

class WeeklyBonus:
    def __init__(self, db):
        self.db = db

    def flag_week_for_recalc(self, date):
        week_start = self.get_week_start(date)
        db.cur.execute("""
            INSERT OR IGNORE INTO WeeklyBonusStatus (week_start)
            VALUES (?)
        """, (week_start,))

        db.cur.execute("""
            UPDATE WeeklyBonusStatus
            SET needs_recalc = 1
            WHERE week_start = ?
        """, (week_start,))
        db.conn.commit()

    def get_week_start(date):
        return date - timedelta(days=date.weekday())
    
    def evaluate_all_weeks(self):
        ...

    def evaluate_week(self, week_start):
        ...

    def weekly_requirements_met(self, week_start, task_name):
        ...

    def award_bonus(self, task_name, week_start):
        ...

    def add_daily_task_weekly_bonus(weekNumber):
        if weekNumber > 3:
            db.cur.execute("UPDATE UserData SET experience = experience + 30")
        else:
            db.cur.execute("UPDATE UserData SET experience = experience + 15")
        db.conn.commit()
    def add_weekly_task_weekly_bonus(weekNumber):
        if weekNumber > 3:
            db.cur.execute("UPDATE UserData SET experience = experience + 50")
        else:
            db.cur.execute("UPDATE UserData SET experience = experience + 30")
        db.conn.commit()
    def remove_daily_task_weekly_bonus(week):
        if week > 3:
            db.cur.execute("UPDATE UserData SET experience = experience - 30")
        else:
            db.cur.execute("UPDATE UserData SET experience = experience - 15")
        db.conn.commit()
    def remove_weekly_task_weekly_bonus(week):
        if week > 3:
            db.cur.execute("UPDATE UserData SET experience = experience - 50")
        else:
            db.cur.execute("UPDATE UserData SET experience = experience - 30")
        db.conn.commit()
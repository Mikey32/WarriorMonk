from data import ActivityDB
from datetime import date, timedelta

db = ActivityDB()

def modify_activity(taskNum, curdate):

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
        add_daily_xp()
    elif answer == 'n':
        db.cur.execute("SELECT sleep FROM Activities WHERE date_val = ?",(curdate,))
        row = db.cur.fetchone()
        sleep = row[0] if row else None
        if sleep == 'good':
            remove_daily_xp()
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
        check_deduct_bool_values_weekly('resistance', curdate)
    else:
        print("Invalid entry")    
        return
    db.conn.commit()
    print("Resistance Updated!")
    return

def modify_steps(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many steps did you do?")
    db.cur.execute("SELECT steps FROM Activities WHERE date_val = ?",(curdate,))
    row = db.cur.fetchone()
    count = row[0] if row else None
    if count < 8000 and int(answer) >= 8000:
        add_daily_xp()
    elif count >= 8000 and int(answer) < 8000:
        remove_daily_xp() 
    db.cur.execute("UPDATE Activities SET steps = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    print("Steps Updated!")
    return

def modifiy_sauna(curdate):
    answer = input("Did you use the sauna today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET sauna = ? WHERE date_val = ?",(True, curdate))
        add_weekly_task_xp()
    elif answer == 'n':
        check_deduct_bool_values_weekly('sauna', curdate)
    else:
        print("Invalid entry")    
        return
    db.conn.commit()
    print("Sauna Updated!")
    return

def modify_cold_plunge(curdate):
    answer = input("Did you cold plunge today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET cold_plunge = ? WHERE date_val = ?",(True, curdate))
        add_daily_xp()
    elif answer == 'n':
        db.cur.execute("SELECT ? FROM Activities WHERE date_val = ?",(cold_plunge, curdate,))
        row = db.cur.fetchone()
        cold_plunge = row[0] if row else None
        if cold_plunge:
            remove_daily_xp()
        db.cur.execute("UPDATE Activities SET cold_plunge = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    db.conn.commit()
    print("Cold Plunge Updated!")
    return

def modify_sprint(curdate):
    answer = input("Did you sprint today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET sprint = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        check_deduct_bool_values_weekly('sprint', curdate)
    else:    
        return "Invalid entry"
    db.conn.commit()
    print("Sprint Updated!")
    return 

def modify_zone2(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many minutes of Zone 2 Cardio did you do?")
    db.cur.execute("SELECT zone2cardio FROM Activities WHERE date_val = ?",(curdate,))
    row = db.cur.fetchone()
    count = row[0] if row else None
    if count < 20 and int(answer) >= 20:
        add_weekly_task_xp()
    elif count >= 20 and int(answer) < 20:
        remove_weekly_task_xp() 
    db.cur.execute("UPDATE Activities SET zone2cardio = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    return "Zone 2 Cardio Updated!"

def modify_meditation(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many minutes of meditation did you do?")
    db.cur.execute("SELECT meditation FROM Activities WHERE date_val = ?",(curdate,))
    row = db.cur.fetchone()
    count = row[0] if row else None
    if count < 5 and int(answer) >= 5:
        add_daily_xp()
    elif count >= 5 and int(answer) < 5:
        remove_daily_xp() 
    db.cur.execute("UPDATE Activities SET meditation = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    print("Meditation Updated!")
    return

def modify_hiit(curdate):
    answer = input("How many minutes of high intensity interval training did you do today?")
    db.cur.execute("SELECT hiit FROM Activities WHERE date_val = ?",(curdate,))
    row = db.cur.fetchone()
    count = row[0] if row else None
    if count < 4 and int(answer) >= 4:
        add_weekly_task_xp()
    elif count >= 4 and int(answer) < 4:
        remove_weekly_task_xp() 
    db.cur.execute("UPDATE Activities SET hiit = ? WHERE date_val = ?",(answer, curdate))
    db.conn.commit()
    return "HIIT Updated!"

def modify_mobility(curdate):
    answer = input("Did you do mobility work today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE Activities SET mobility = ? WHERE date_val = ?",(True, curdate))
        add_weekly_task_xp()
    elif answer == 'n':
        check_deduct_bool_values_weekly('mobility', curdate)
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

def check_deduct_bool_values_weekly(type, curdate):
    db.cur.execute("SELECT ? FROM Activities WHERE date_val = ?",(type, curdate,))
    row = db.cur.fetchone()
    attribute = row[0] if row else None
    if attribute:
        remove_weekly_task_xp()
    db.cur.execute("UPDATE Activities SET ? = ? WHERE date_val = ?",(type, False, curdate))
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
        db.cur.execute("""
            SELECT week_start
            FROM WeeklyBonusStatus
            WHERE needs_recalc = 1
        """)
        weeks = [row[0] for row in db.cur.fetchall()]
        for week_start in weeks:
            self.evaluate_week(week_start)


    def evaluate_week(self, week_start):
        #Insert into DB at the end total points into bonus weeks.
        sleep_bonus = self.calculate_sleep_weekly_bonus(week_start)
        if sleep_bonus > 0:
            print(f"Congratulations! {sleep_bonus} bonus points awarded for consistently good sleep.")
        resistance_bonus = self.calculate_resistance_weekly_bonus(week_start)
        if resistance_bonus > 0:
            print(f'Congratulations! {resistance_bonus} bonus points awarded for consistently doing resistance training.')
        steps_bonus = self.calculate_steps_weekly_bonus(week_start)
        if steps_bonus > 0:
            print(f'Congratulations! {steps_bonus} bonus points awarded for steps!')
        sauna_bonus = self.calculate_sauna_weekly_bonus(week_start)
        if sauna_bonus > 0:
            print(f'Congratulations! {sauna_bonus} points awarded for using the sauna.')
        cold_plunge_bonus = self.calculate_cold_plunge_bonus(week_start)
        if cold_plunge_bonus > 0:
            print(f'Congratulations! {cold_plunge_bonus} points awareded for consitent cold plunging. Extra points awarded because 6 days out of 7 of doing a cold plung is insane.')
        hiit_bonus = self.calculate_hiit_weekly_bonus(week_start)
        if hiit_bonus > 0:
            print(f'Congratulations! {hiit_bonus} points awarded for hiit training!')
        meditiation_bonus = self.calculate_meditation_weekly_bonus(week_start)
        if meditiation_bonus > 0:
            print(f'Congratulations! {meditiation_bonus} points awarded for meditating!')
        sprint_bonus = self.calculate_sprint_bonus(week_start)
        if sprint_bonus > 0:
            print(f'Congratulations! {sprint_bonus} awarded for sprinting.')
        mobility_bonus = self.calculate_mobility_weekly_bonus(week_start)
        if mobility_bonus > 0:
            print(f'Congratulations! {mobility_bonus} awarded for doing some mobility.')
        total = sleep_bonus + resistance_bonus + steps_bonus + sauna_bonus + cold_plunge_bonus + hiit_bonus + meditiation_bonus + sprint_bonus + mobility_bonus
        db.cur.execute("""
            UPDATE WeeklyBonusStatus
            SET needs_recalc = 0,
                bonus_awarded = ?
            WHERE week_start = ?
        """, (total, week_start,))
        db.conn.commit()

    def weekly_requirements_met(self, week_start, task_name):
        ...

    def award_bonus(self, task_name, week_start):
        ...

    # Putting a separate function here for now. Will plug into weekly requirements if it is small enough:
    def calculate_sleep_weekly_bonus(week_start):
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                        AND sleep = 'good'
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > 5:
            bonus_tracker += 15
            db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                        AND sleep = 'good'
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > 5:
                bonus_tracker += 30
            return bonus_tracker
        else:
            return 0
    def calculate_resistance_weekly_bonus(week_start):
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                        AND resistance = True
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > 1:
            bonus_tracker += 30
            db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                        AND resistance = True
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > 1:
                bonus_tracker += 50
            return bonus_tracker
        else:
            return 0
        
    def calculate_steps_weekly_bonus(week_start):
        steps_bonus_threshold = 48000
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT SUM(steps)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > steps_bonus_threshold:
            bonus_tracker += 15
            db.cur.execute("""
                        SELECT SUM(steps)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > steps_bonus_threshold:
                bonus_tracker += 30
            return bonus_tracker
        else:
            return 0
    def calculate_sauna_weekly_bonus(week_start):
        sauna_threshold = 0
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                        AND sauna = True
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > sauna_threshold:
            bonus_tracker += 30
            db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                        AND sauna = True
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > sauna_threshold:
                bonus_tracker += 50
            return bonus_tracker
        else:
            return 0
    def calculate_cold_plunge_bonus(week_start):
        cold_plunge_threshold = 5
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                        AND cold_plunge = True
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > cold_plunge_threshold:
            bonus_tracker += 30
            db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                        AND cold_plunge = True
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > cold_plunge_threshold:
                bonus_tracker += 50
            return bonus_tracker
        else:
            return 0
    def calculate_sprint_bonus(week_start):
        sprint_threshold = 0
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                        AND sprint = True
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > sprint_threshold:
            bonus_tracker += 30
            db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                        AND sprint = True
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > sprint_threshold:
                bonus_tracker += 50
            return bonus_tracker
        else:
            return 0
    def calculate_hiit_weekly_bonus(week_start):
        hiit_threshold = 19
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT SUM(hiit)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > hiit_threshold:
            bonus_tracker += 30
            db.cur.execute("""
                        SELECT SUM(hiit)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > hiit_threshold:
                bonus_tracker += 50
            return bonus_tracker
        else:
            return 0
    def calculate_zone2_weekly_bonus(week_start):
        zone2_threshold = 150
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT SUM(zone2cardio)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > zone2_threshold:
            bonus_tracker += 30
            db.cur.execute("""
                        SELECT SUM(zone2cardio)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > zone2_threshold:
                bonus_tracker += 50
            return bonus_tracker
        else:
            return 0
    def calculate_meditation_weekly_bonus(week_start):
        meditation_threshold = 6
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                        AND meditation = True
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > meditation_threshold:
            bonus_tracker += 15
            db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                        AND sauna = True
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > meditation_threshold:
                bonus_tracker += 30
            return bonus_tracker
        else:
            return 0
    
    def calculate_mobility_weekly_bonus(week_start):
        mobility_threshold = 1
        bonus_tracker = 0
        db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-7 days') AND DATE(?,'-1 day')
                        AND mobility = True
                    """, (week_start, week_start))
        count_good = db.cur.fetchone()[0]
        if count_good > mobility_threshold:
            bonus_tracker += 30
            db.cur.execute("""
                        SELECT COUNT(*)
                        FROM Activities
                        WHERE date_val BETWEEN DATE(?,'-14 days') AND DATE(?,'-7 days')
                        AND resistance = True
                    """, (week_start, week_start))
            count_good_prev_week = db.cur.fetchone()[0]
            if count_good_prev_week > 1:
                bonus_tracker += 50
            return bonus_tracker
        else:
            return 0

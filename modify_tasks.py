from data import ActivityDB
from datetime import date

db = ActivityDB()

def modify_sleep(curdate):
    answer = input("How was your sleep?(y = good, n = not good)")
    if answer == 'y':
        db.cur.execute("UPDATE activities SET sleep = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE activities SET sleep = ? WHERE date_val = ?",(False, curdate))
    else:
        return "Invalid entry"
    return "Sleep Updated!"

def modify_resistance(curdate):
    answer = input("Did you do resistance?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE activities SET resistance = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE activities SET resistance = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    return "Resistance Updated!"

def modify_steps(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many steps did you do?")
    db.cur.execute("UPDATE activities SET steps = ? WHERE date_val = ?",(answer, curdate))
    return "Steps Updated!"

def modifiy_sauna(curdate):
    answer = input("Did you use the sauna today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE activities SET sauna = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE activities SET sauna = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    return "Sauna Updated!"

def modify_cold_plunge(curdate):
    answer = input("Did you cold plunge today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE activities SET cold_plunge = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE activities SET cold_plunge = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    return "Cold Plunge Updated!"

def modify_sprint(curdate):
    answer = input("Did you sprint today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE activities SET sprint = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE activities SET sprint = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    return "Sprint Updated!"

def modify_zone2(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many minutes of Zone 2 Cardio did you do?")
    db.cur.execute("UPDATE activities SET zone2cardio = ? WHERE date_val = ?",(answer, curdate))
    return "Zone 2 Cardio Updated!"

def modify_meditation(curdate):
    #ToDo: Check if it's an integer
    answer = input("How many minutes of meditation did you do?")
    db.cur.execute("UPDATE activities SET meditation = ? WHERE date_val = ?",(answer, curdate))
    return "Meditation Updated!"

def modify_core(curdate):
    answer = input("Did you do a core workout today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE activities SET core = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE activities SET core = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    return "Core Updated!"

def modify_mobility(curdate):
    answer = input("Did you do mobility work today?(y = yes, n = no)")
    if answer == 'y':
        db.cur.execute("UPDATE activities SET mobility = ? WHERE date_val = ?",(True, curdate))
    elif answer == 'n':
        db.cur.execute("UPDATE activities SET mobility = ? WHERE date_val = ?",(False, curdate))
    else:    
        return "Invalid entry"
    return "Mobility Updated!"





# db.cur.execute("INSERT INTO UserData (name) VALUES (?)", (name,))

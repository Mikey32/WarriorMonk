from datetime import date


def main():
#Display current date and what has been accomplished.
    sleep = "Unknown"
    resistance = "not done"
    sauna = "not done"
    plunge = "not done"
    sprint = "not done"
    cardio = 0
    meditation = 0
    core = "not done"
    mobility = "not done"
    print("Good Morning. Today is " + str(date.today()))
    print("Last nights sleep was " + sleep)
    print("Today you have  " + resistance + " resistance training")
    print("You have "+ sauna + " sauna.")
    print("You have " + plunge + " cold plunged.")
    print("You have " + sprint + " sprinted")
    print("You have done " + str(cardio) + " minutes of zone 2 cardio.")
    print("You meditated for "+ str(meditation) +" minutes.")
    print("You have " + core + "core work.")
    print("You have " + mobility + "mobility work.")





if __name__ == "__main__":
    main()

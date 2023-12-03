# This file contains all the mini functions used to calculate the probabilites with each parent

    #     input_interactivity = input("\n Enter your class's interactivity. 0 = some class participation, but not much interaction between classmates. 1 = introsems, classes with 60 people or fewer, or lectures with 2-3 breakouts or pollEvs. Enter 1 or 0:  ")

def p_interactivity(attendance): 
    # P(interactivity = 1 | Attendance = attendance)
    if attendance == 0: return 0.05 # if you don't attend class, there's gonna be minimal interactions, maybe only through ed or pset partners
    if attendance == 1: return 0.95

    else:
        print("Invalid attendance value:", attendance)
        return 0.0

def p_strangers(frequency, size, attendance): 
    # 0 = you don't go in-person to classes or you never sit next to anyone new in lecture. 1 = you sit next to at least one other new person in lecture.
    # P(strangers = 1 | Frequency = frequency, Size = size, Attendance = attendance)
    if frequency == 0 and size == 0 and attendance == 0: return 0.01 # small size, once a week, no attendance
    if frequency == 0 and size == 0 and attendance == 1: return 0.80 # small size, once a week, attend
    if frequency == 0 and size == 1 and attendance == 0: return 0.01 # Big class, once a week, no attendance
    if frequency == 0 and size == 1 and attendance == 1: return 0.20 # Big class, once a week, attend
    if frequency == 1 and size == 0 and attendance == 0: return 0.10 # Small class, many meetings, no attendance
    if frequency == 1 and size == 0 and attendance == 1: return 0.98 # Small class, many meetings, attendance
    if frequency == 1 and size == 1 and attendance == 0: return 0.15 # big class, many meetings, no attendance
    if frequency == 1 and size == 1 and attendance == 1: return 0.95 # big class, many meetings, attendance
    else:
        print("Invalid combination of frequency, size, and attendance:", frequency, size, attendance)
        return 0.0

def p_20(strangers, interactivity): # meeting fewer people
    # P(You meet around 20 or fewer people | Strangers = strangers, Interactivity = interactivity)
    if strangers == 1 and interactivity == 1: return 0.10 # Strangers, lots of interact
    if strangers == 0 and interactivity == 1: return 0.30 # No strangers, lots of interact
    if strangers == 1 and interactivity == 0: return 0.40 # Strangers, no interact
    if strangers == 0 and interactivity == 0: return 0.98 # No strangers, no interactivity
    else:
        print("Invalid combination of strangers and interactivity: ", strangers, interactivity)
        return 0.0

def p_30(strangers, interactivity): # meeting average amount of people
    # P(You meet around 30 more people | Strangers = strangers, Interactivity = interactivity)
    if strangers == 1 and interactivity == 1: return 0.50 
    if strangers == 0 and interactivity == 1: return 0.55
    if strangers == 1 and interactivity == 0: return 0.30
    if strangers == 0 and interactivity == 0: return 0.20
    else:
        print("Invalid combination of strangers and interactivity: ", strangers, interactivity)
        return 0.0

def p_40(strangers, interactivity): # meeting the greatest people
    # P(You meet around 40 more people | Strangers = strangers, Interactivity = interactivity)
    if strangers == 1 and interactivity == 1: return 0.95
    if strangers == 0 and interactivity == 1: return 0.60
    if strangers == 1 and interactivity == 0: return 0.50
    if strangers == 0 and interactivity == 0: return 0.10
    else:
        print("Invalid combination of strangers and interactivity: ", strangers, interactivity)
        return 0.0




    



    
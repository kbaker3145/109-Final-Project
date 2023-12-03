import math
import numpy as np
from scipy import stats
from scipy.stats import bernoulli

# Exporting from other project file
from parent_rvs import p_interactivity
from parent_rvs import p_strangers
from parent_rvs import p_20
from parent_rvs import p_30
from parent_rvs import p_40


# CONSTANTS
N_SAMPLES = 20000
AVERAGE_PEOPLE_SEEN = 250
CURRENT_FRIENDS = 100

P_ATTENDANCE = 0.55 # It is usually around 1/3 (according to Prof. Piech). I'm being optimistic
P_CLASS_FREQ = 0.80 # Majority of Stanford classes meet 2-3 times a week
P_CLASS_SIZE = 0.50 # Majority of Stanford classes are smaller, but the bigger classes are more popular. 

"""
Helpers for checking number validity 
"""
def is_number(variable):
    return isinstance(variable, (int))

def is_valid_number(s):
    try:
        int_value = int(s)
        return True
    except ValueError:
        return False

"""
Gathers inputs from the user on school size, class frequency, class size, and personal attedance. 
"""
def gather_user_info():

    res = {}

    # get school size
    while True: 
        input_school_size = input("\n Enter your school size:  ")
        if not is_valid_number(input_school_size):
            print("\n That wasn't a valid input! Enter an integer. \n")
        elif int(input_school_size) < AVERAGE_PEOPLE_SEEN:
            print("\n No way your college is this small. Be realistic -- try again: \n")
        else:
            break
    res["input_school_size"] = int(input_school_size)
    # get class frequency
    while True: 
        input_class_frequency = input("\n Enter your class's meeting frequency. 0 = once a week, no section. 1 = 2 times a week with section, or 3 times a week. Enter 1 or 0:  ")
        if input_class_frequency != "1" and input_class_frequency != "0":
            print("That wasn't a valid input! Enter 0 or 1. \n")
        else:
            break
    res["input_class_frequency"] = int(input_class_frequency)
    # get class size
    while True: 
        input_class_size = input("\n Enter your class size. 0 = introsems, classes with 60 people or fewer. 1 = any larger courses (over 60). Enter 1 or 0:  ")
        if input_class_size != "1" and input_class_size != "0":
            print("That wasn't a valid input! Enter 0 or 1. \n")
        else:
            break
    res["input_class_size"] = int(input_class_size)
    # get attendance
    while True: 
        input_attendance = input("\n Now the last and most important! Enter how often you attend lectures in-person. 0 = you don't go in-person or you attending less than 60% of lectures. 1 = you attend about 60% or more of your lectures in person. Enter 1 or 0:  ")
        if input_attendance != "1" and input_attendance != "0":
            print("That wasn't a valid input! Enter 0 or 1. \n")
        elif input_attendance == "1":
            print("\n Amazing job with that attendance :) \n")
            break
        else:
            break
    res["input_attendance"] = int(input_attendance)
    return res

"""   
Returns a dictionary of probabilities knowing 20, 30, or 40 more people given the other nodes in the Bayesian Network.
"""
def get_probs_and_max(d):

    # getting second layer
    prob_interactivity = p_interactivity(d["input_attendance"])
    prob_strangers = p_strangers(d["input_class_frequency"], d["input_class_size"], d["input_attendance"])
    
    # get bernoulli samples
    b_prob_interactivity = bernoulli(prob_interactivity)
    b_prob_strangers = bernoulli(prob_strangers)
    strangers_sample = b_prob_strangers.rvs()
    interactivity_sample = b_prob_interactivity.rvs()

    # getting third layer
    prob_20 = p_20(strangers_sample, interactivity_sample)
    prob_30 = p_30(strangers_sample, interactivity_sample)
    prob_40 = p_40(strangers_sample, interactivity_sample)

    # return the max number of friends from the probability
    max_prob = max([prob_20, prob_30, prob_40])
    res = {prob_20: 20, prob_30: 30, prob_40: 40}
    return res[max_prob]


"""
This function leverages the conditional independence between 2 nodes in the bayesian network to find 
the probability of the current outcomes of strangers next to you, your attendance, and your class' interactivity: 
P(attendance, interactivity, strangers). 

This is primarily to explore the nature of conditional independence and doesn't have a direct influence on the 
serendipity problem. 
"""
def conditional_independance(d):
    while (True):
        prob_input = input("\n Want to find the probability of the number of new friends you (could've) made by sitting next to new classmates (with the class' interactivity and attendance?) Enter Y or N: \n")
        if prob_input.lower() != "y" and prob_input.lower() != "n":
            print("That wasn't a valid input! Enter y or n. \n")
        elif prob_input.lower() == "n":
            print("\n No worries! Thanks for participating \n")
            return
        else:
            break
    input_attendance = d["input_attendance"]
    b_prob_attend = bernoulli(P_ATTENDANCE)
    b_prob_size = bernoulli(P_CLASS_SIZE)
    b_prob_freq = bernoulli(P_CLASS_FREQ)

    sample_attend = b_prob_attend.rvs()
    p_attend = P_ATTENDANCE
    if sample_attend == 0:
        p_attend = 1 - P_ATTENDANCE
    sample_size = b_prob_size.rvs()
    p_size = P_CLASS_SIZE
    if sample_size == 0:
        p_size = 1 - P_CLASS_SIZE
    sample_freq = b_prob_freq.rvs()
    p_freq = P_CLASS_FREQ
    if sample_freq == 0:
        p_freq = 1 - P_CLASS_FREQ

    prob_strangers_interactivity_attendance = p_attend * p_size * p_freq * p_strangers(sample_freq, sample_size, sample_attend) * p_interactivity(sample_attend)
    
    print("\n The probability of you sitting next to strangers, attending class, and being in an interactive class is: ", round(prob_strangers_interactivity_attendance, 8), "\n")
    return

# Computing serendipity -- probability that you see no friends
def serendipity(curr_friends, new_friends, school_size):

    total_friends = curr_friends + new_friends
    denom = math.comb(school_size, AVERAGE_PEOPLE_SEEN)
    nume = math.comb((school_size - total_friends), AVERAGE_PEOPLE_SEEN)

    return(nume/denom)


def main():

    class_number = 1  # Initialize the class number
    new_friends = 0 # keep a running total of the friends made from classes

    while True:
        print(f"\nClass {class_number}:\n")
        d = gather_user_info()
        new_friends += get_probs_and_max(d)
        prob_before = 1 - serendipity(CURRENT_FRIENDS, 0, d["input_school_size"])
        prob_after = 1 - serendipity(CURRENT_FRIENDS, new_friends, d["input_school_size"])

        increase = ((prob_after - prob_before) / prob_after) * 100
        print("\nFriends before: ", CURRENT_FRIENDS)
        print("\nFriends after: ", new_friends + CURRENT_FRIENDS)
        print("\nSchool size: ", d["input_school_size"])
        print("\nOut of", AVERAGE_PEOPLE_SEEN, "people seen, the probability that you see at least one friend is", round((prob_after), 2), "! \n")
        print("This is a(n)", round(increase, 2), "percent increase than if you hadn't met anyone in class. Way to go! :)")
        conditional_independance(d)

        # Ask the user if they want to input another class
        another_class = input("Do you want to input another class? Enter Y or N: ")
        if another_class.lower() != 'y':
            print("\n Thank you for participating!")
            break  # Exit the loop if the user doesn't want to input another class

        class_number += 1  # Increment the class number


if __name__ == "__main__":
    main()








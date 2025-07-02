# main.py
from weeks.week_1.day2 import intro_to_ai
from weeks.week_2.day1 import intro_to_numpy


def main():
    print("=== AI Bootcamp Dashboard ===")
    print("1. Week 1 - Introduction to AI")
    print("2. Week 2 - Numpy ")
    
    choice = input("Enter week number (1 or 2): ")
    if choice == "1":
        intro_to_ai()
    elif choice == "2":
        intro_to_numpy()
    else:
        print("Invalid choice")

if __name__ =="__main__":
     main()
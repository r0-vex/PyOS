import random
import winsound

gen_number=random.randint(1,100)
print("Guess a number between 1-100")
def easy():
    for i in range(8,0,-1):
        print("Chances Remaining:",i-1)
        try:
            guess=int(input("PyOS:/home/user/apps/guess> "))
        except ValueError:
            print("ValueError: ENTER NUMBERS")
        except Exception as GuessError:
            print("ERROR:",GuessError)
        if guess==gen_number:
            print("YAY! YOU WIN")
            print("The number is",gen_number)
            break
        elif guess<gen_number:
            winsound.Beep(400,1000)
            print("Your Guess is low\n")
        else:
            winsound.Beep(400,1000)
            print("Your Guess is high\n")
    else:
        print("Game over,the number was",gen_number)
def hard():
    for i in range(5,0,-1):
        print("Chances Remaining:",i-1)
        try:
            guess=int(input("PyOS:/home/user/apps/guess> "))
        except ValueError:
            print("ValueError: ENTER NUMBERS")
        except Exception as GuessError:
            print("ERROR:",GuessError)
        if guess==gen_number:
            print("YAY! YOU WIN")
            print("The number is",gen_number)
            break
        elif guess<gen_number:
            winsound.Beep(400,1000)
            print("Your Guess is low\n")
        else:
            winsound.Beep(400,1000)
            print("Your Guess is high\n")
    else:
        print("Game over the number was:",gen_number)
def menu():
    print("1.EASY LEVEL")
    print("2.HARD LEVEL")
    print("3.EXIT")

while True:
    menu()
    try:
        choice=int(input("\nPyOS:/home/user/apps/guess/option> "))
        if choice==1:
            easy()
        elif choice==2:
            hard()
        elif choice==3:
            print("Exiting")
            break
        else:
            print(f"Can't find {choice} try to select from 1-2")
    except ValueError:
        print("ValueError: ENTER NUMBERS")
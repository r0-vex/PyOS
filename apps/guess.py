import random
import winsound
import time
import json
import os

APP_PATH="guess"
DEF_SCORE_FILE={"easy":0,"hard":0,"very_hard":0}
score_dict={}
cache=[]

def main(username,path):
    try:
        if not (os.path.isdir(f"{path}\\{APP_PATH}")):
            os.mkdir(f"{path}\\{APP_PATH}")
        if not (os.path.isfile(f"{path}\\{APP_PATH}\\scores.json")):
            with open(path+f"\\{APP_PATH}\\scores.json","w") as source:
                source.write(json.dumps(DEF_SCORE_FILE))
    except Exception as GUESSError:
        print(f"GUESS APP ERROR: {GUESSError}")

    def load_score():
        global score_dict
        try:
            with open(path+f"\\{APP_PATH}\\scores.json") as score_json:
                score_dict=json.loads(score_json.read())
        except FileNotFoundError:
            print("Scores can't be loaded!")
        except Exception as ScoreError:
            print(f"Score File Error: {ScoreError}")
    
    def dump_score():
        global score_dict
        try:
            with open(path+f"\\{APP_PATH}\\scores.json","w") as score_json:
                score_json.write(json.dumps(score_dict))
        except FileNotFoundError:
            print("Scores can't be updated!")
        except Exception as ScoreError:
            print(f"Score File Error: {ScoreError}")

    def hint(number, mode, guessed=None):
        global cache
        if mode=="easy":
            hint_type = random.choice(["OE", "MOD", "GT"])
            if hint_type in cache:
                return None
            cache.append(hint_type)
            if hint_type=="OE":
                return "I'm an EVEN number." if number % 2 == 0 else "I'm an ODD number."
            elif hint_type=="MOD":
                divisors = [7, 5, 3, 2]
                for divisor in divisors:
                    if number % divisor==0:
                        return f"I'm divisible by {divisor}."
                if number==1:
                    return "Every number is divisible by me ;)"
                return "I'm a Prime Number ;)"
            elif hint_type=="GT":
                return "I'm less than 50." if number < 50 else "I'm greater than 50."
        elif mode=="hard":
            if guessed is None:
                return "No guess provided for hard mode. (Try guessing something!!)"
            hint_type = random.choice(["RANGE", "DIFF"])
            if hint_type in cache:
                return None
            cache.append(hint_type)
            if hint_type=="RANGE":
                lower= max(1, number - 10)
                upper= min(100, number + 10)
                return f"I'm within the range of {lower} to {upper}."
            elif hint_type=="DIFF":
                difference =abs(number - guessed)
                if difference <= 5:
                    return "You're EXTREMELY close!"
                elif difference <= 10:
                    return "You're very close."
                elif difference <= 20:
                    return f"You're within {difference}."
                return "You're far away from the target."
        elif mode == "very_hard":
            if guessed is None:
                return "No guess provided for very hard mode.(Try some guess!!)"
            difference = abs(number - guessed)
            if difference <= 3:
                return "BURNING HOT"
            elif difference <= 7:
                return "VERY HOT"
            elif difference <= 15:
                return "WARM"
            elif difference <= 30:
                return "COLD"
            return "FREEZING"
        return "Invalid Hint Mode"

    print(r""" $$$$$$\  $$\   $$\ $$$$$$$$\  $$$$$$\   $$$$$$\  
$$  __$$\ $$ |  $$ |$$  _____|$$  __$$\ $$  __$$\ 
$$ /  \__|$$ |  $$ |$$ |      $$ /  \__|$$ /  \__|
$$ |$$$$\ $$ |  $$ |$$$$$\    \$$$$$$\  \$$$$$$\  
$$ |\_$$ |$$ |  $$ |$$  __|    \____$$\  \____$$\ 
$$ |  $$ |$$ |  $$ |$$ |      $$\   $$ |$$\   $$ |
\$$$$$$  |\$$$$$$  |$$$$$$$$\ \$$$$$$  |\$$$$$$  |
 \______/  \______/ \________| \______/  \______/ """)

    def easy():
        score,used_hint,i=150,0,8
        last_guess=None
        global cache
        cache.clear()
        gen_number=random.randint(1,100)
        print("Guess a number between 1-100")
        while i>0:
            print("\nChances Remaining:",i-1)
            try:
                guess=input("Your Guess: ")
                if guess.lower()=="hint":
                    if used_hint>1:
                        print("No more hints!!")
                        continue
                    while True:
                        gen_hint=hint(gen_number,"easy",last_guess)
                        if gen_hint is not None:
                            break
                    print(f"Hint: {gen_hint}")
                    i-=1
                    used_hint+=1
                    score-=5
                    continue
                guess=int(guess)
                last_guess=guess
            except ValueError:
                print("ValueError: ENTER ONLY NUMBERS")
                continue
            except Exception as GuessError:
                print("ERROR:",GuessError)
                continue
            if guess==gen_number:
                print("YAY! YOU WON!!")
                print("I'm",gen_number)
                print(f"Your Score: {score}")
                load_score()
                if score_dict["easy"]<score:
                    score_dict["easy"]=score
                    dump_score()
                break
            elif guess<gen_number:
                i-=1
                score-=10
                winsound.Beep(400,500)
                print("I'm higher than your guess.")
            else:
                i-=1
                score-=10
                winsound.Beep(400,500)
                print("I'm lower than your guess.")
        else:
            print("Game over,I'm",gen_number)
            print("Your Score:",score)

    def hard():
        score,used_hint,i=150,0,5
        last_guess=None
        global cache
        cache.clear()
        gen_number=random.randint(1,100)
        print("Guess a number between 1-100")
        while i>0:
            print("\nChances Remaining:",i-1)
            try:
                guess=input("Your Guess: ")
                if guess.lower()=="hint":
                    if used_hint>1:
                        print("No more hints!!")
                        continue
                    while True:
                        gen_hint=hint(gen_number,"hard",last_guess)
                        if gen_hint is not None:
                            break
                    print(f"Hint: {gen_hint}")
                    i-=1
                    used_hint+=1
                    score-=10
                    continue
                guess=int(guess)
                last_guess=guess
            except ValueError:
                print("ValueError: ENTER ONLY NUMBERS")
                continue
            except Exception as GuessError:
                print("ERROR:",GuessError)
                continue
            if guess==gen_number:
                print("YAY! YOU WON!!")
                print("I'm",gen_number)
                print(f"Your Score: {score}")
                load_score()
                if score_dict["hard"]<score:
                    score_dict["hard"]=score
                    dump_score()
                break
            elif guess<gen_number:
                i-=1
                score-=20
                winsound.Beep(400,500)
                print("I'm higher than your guess.")
            else:
                i-=1
                score-=20
                winsound.Beep(400,500)
                print("I'm lower than your guess.")
        else:
            print("Game over,I'm",gen_number)
            print("Your Score:",score)

    def very_hard():
        score,used_hint,i=150,0,4
        last_guess=None
        print("Guess a number between 1-100")
        gen_number=random.randint(1,100)
        while i>0:
            print("\nChances Remaining:",i-1)
            try:
                guess=input("Your Guess: ")
                if guess.lower()=="hint":
                    if used_hint>1:
                        print("No more hints!!")
                        continue
                    while True:
                        gen_hint=hint(gen_number,"very_hard",last_guess)
                        if gen_hint is not None:
                            break
                    print(f"Hint: {gen_hint}")
                    i-=1
                    used_hint+=1
                    score-=15
                    continue
                guess=int(guess)
                last_guess=guess
            except ValueError:
                print("ValueError: ENTER ONLY NUMBERS")
                continue
            except Exception as GuessError:
                print("ERROR:",GuessError)
                continue
            if guess==gen_number:
                print("YAY! YOU WON!!")
                print("I'm",gen_number)
                print(f"Your Score: {score}")
                load_score()
                if score_dict["very_hard"]<score:
                    score_dict["very_hard"]=score
                    dump_score()
                break
            elif guess<gen_number:
                i-=1
                score-=25
                winsound.Beep(400,500)
                print("I'm higher than your guess.")
            else:
                i-=1
                score-=25
                winsound.Beep(400,500)
                print("I'm lower than your guess.")
        else:
            print("Game over,I'm",gen_number)
            print("Your Score:",score)

    def view_score():
        load_score()
        print("\n ### HIGH SCORES ###\n")
        print("Easy:",score_dict["easy"])
        print("Hard:",score_dict["hard"])
        print("Very Hard:",score_dict["very_hard"])
        print("\n ###     ###\n")

    def menu():
        print("\n1.EASY LEVEL")
        print("2.HARD LEVEL")
        print("3.VERY HARD LEVEL")
        print("4.VIEW HIGH SCORE")
        print("5.EXIT")
#MAIN LOOP
    while True:
        menu()
        try:
            choice=int(input(f"\nPyOS:/home/{username}/apps/guess/option> "))
            if choice==1:
                easy()
            elif choice==2:
                hard()
            elif choice==3:
                very_hard()
            elif choice==4:
                view_score()
            elif choice==5:
                print("Exiting. ",end="")
                for _ in range(2):
                    time.sleep(0.5)
                    print(". ",end="",flush=True)
                print()
                return "Exited!"
            else:
                print(f"Can't find {choice} try to select from 1-5")
        except ValueError:
            print("ValueError: ENTER NUMBERS")
        except Exception as GuessError:
            print(f"ERROR: {GuessError}")
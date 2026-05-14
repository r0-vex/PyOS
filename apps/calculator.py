import time

def main(username,path):

    print(r"""   _____          _      _____ _    _ _            _______ ____  _____  
  / ____|   /\   | |    / ____| |  | | |        /\|__   __/ __ \|  __ \ 
 | |       /  \  | |   | |    | |  | | |       /  \  | | | |  | | |__) |
 | |      / /\ \ | |   | |    | |  | | |      / /\ \ | | | |  | |  _  / 
 | |____ / ____ \| |___| |____| |__| | |____ / ____ \| | | |__| | | \ \ 
  \_____/_/    \_\______\_____|\____/|______/_/    \_\_|  \____/|_|  \_\ """)

    def add(a,b):
        return a+b
    def sub(a,b):
        return a-b
    def multiply(a,b):
        return a*b
    def divide(a,b):
        try:
            return a/b
        except ZeroDivisionError:
            return "Cannot divide by zero"
        except Exception as CalcError:
            return f"ERROR: {CalcError}"
    def menu():
        print("\n0.View Menu")
        print("1.Addition")
        print("2.Subtraction")
        print("3.Multiplication")
        print("4.Division")
        print("5.Square")
        print("6.Square Root")
        print("7.Exit")

#MAIN LOOP
    menu()
    while True:
        try:
            choice= int(input(f"\nPyOS:/home/{username}/apps/calculator/option> "))
            if choice==0:
                menu()
            elif choice==1:
                a=int(input("ADD> "))
                b=int(input("ADD> "))
                print("Result>",add(a,b))
            elif choice==2:
                a=int(input("SUB> "))
                b=int(input("SUB> "))
                print("Result>",sub(a,b))
            elif choice==3:
                a=int(input("MUL> "))
                b=int(input("MUL> "))
                print("Result>",multiply(a,b))
            elif choice==4:
                a=int(input("DIV> "))
                b=int(input("DIV> "))
                print("Result>",divide(a,b))
            elif choice==5:
                a=int(input("SQUARE> "))
                print("Result>",a*a)
            elif choice==6:
                a=int(input("SQRT> "))
                print("Result>",a**0.5)
            elif choice==7:
                print("Exiting...")
                time.sleep(1)
                return "Exited"
            else:
                print(f"Can't find {choice} try to select from 1-7")
        except ValueError:
            print("ValueError: ENTER NUMBERS")
        except Exception as CalcError:
            print("ERROR:",CalcError)
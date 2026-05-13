import time

print(r"""  / ____|    | |          | |     | |            
 | |     __ _| | ___ _   _| | __ _| |_ ___  _ __ 
 | |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|
 | |___| (_| | | (__| |_| | | (_| | || (_) | |   
  \_____\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   """)

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
def menu():
    print("\n0.View Menu")
    print("1.Addition")
    print("2.Subtraction")
    print("3.Multiplication")
    print("4.Division")
    print("5.Square")
    print("6.Square Root")
    print("7.Exit")

menu()
while True:
    try:
        choice= int(input("\nPyOS:/home/user/apps/calculator/option> "))
        if choice==0:
            menu()
        elif choice==1:
            a=int(input("PyOS:/home/user/apps/calculator/add> "))
            b=int(input("PyOS:/home/user/apps/calculator/add> "))
            print("PyOS:/home/user/apps/calculator/add/result>",add(a,b))
        elif choice==2:
            a=int(input("PyOS:/home/user/apps/calculator/sub> "))
            b=int(input("PyOS:/home/user/apps/calculator/sub> "))
            print("PyOS:/home/user/apps/calculator/sub/result>",sub(a,b))
        elif choice==3:
            a=int(input("PyOS:/home/user/apps/calculator/mul> "))
            b=int(input("PyOS:/home/user/apps/calculator/mul> "))
            print("PyOS:/home/user/apps/calculator/mul/result>",multiply(a,b))
        elif choice==4:
            a=int(input("PyOS:/home/user/apps/calculator/div> "))
            b=int(input("PyOS:/home/user/apps/calculator/div> "))
            print("PyOS:/home/user/apps/calculator/div/result>",divide(a,b))
        elif choice==5:
            a=int(input("PyOS:/home/user/apps/calculator/square> "))
            print("PyOS:/home/user/apps/calculator/square/result>",a*a)
        elif choice==6:
            a=int(input("PyOS:/home/user/apps/calculator/sqrt> "))
            print("PyOS:/home/user/apps/calculator/sqrt/result>",a**0.5)
        elif choice==7:
            print("Exiting...")
            time.sleep(2)
            print("Exit Successful....\n")
            break
        else:
            print(f"Can't find {choice} try to select from 1-7")
    except ValueError:
        print("ValueError: ENTER NUMBERS")
    except Exception as CalcError:
        print("ERROR:",CalcError)
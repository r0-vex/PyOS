import time

def menu():
    print("1.USD->INR")
    print("2.GBP->INR")
    print("3.EUROS->INR")
    print("4.AED->INR")
    print("5.CAD->INR")
    print("6.EXIT")


while True:
    menu()
    try:
        choice=int(input("\nPyOS:/home/user/apps/currency_converter/option> "))
        if choice==1:
            amt=int(input("PyOS:/home/user/apps/currency_converter/usd> "))
            print("PyOS:/home/user/apps/currency/amount/inr>",amt*90)
        elif choice==2:
            amt=int(input("PyOS:/home/user/apps/currency_converter/gbp> "))
            print("PyOS:/home/user/apps/currency/amount/inr>",amt*120)
        elif choice==3:
            amt=int(input("PyOS:/home/user/apps/currency_converter/euros> "))
            print("PyOS:/home/user/apps/currency/amount/inr>",amt*105)
        elif choice==4:
            amt=int(input("PyOS:/home/user/apps/currency_converter/aed> "))
            print("PyOS:/home/user/apps/currency/amount/inr>",amt*24)
        elif choice==5:
            amt=int(input("PyOS:/home/user/apps/currency_converter/cad> "))
            print("PyOS:/home/user/apps/currency/amount/inr>",amt*64)
        elif choice==6:
            print("Exiting...")
            time.sleep(2)
            print("Exit Successful....\n")
            break
        else:
            print("INVALID CHOICE")
    except ValueError:
        print("ValueError: ENTER NUMBER")
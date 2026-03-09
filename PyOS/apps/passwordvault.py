import time
import os

APP_PATH="pv"

def main(username,path):
    if not (os.path.isdir(f"{path}\\{APP_PATH}")):
        os.mkdir(f"{path}.{APP_PATH}")

    print(r""" ____                                     _  __     __          _ _   
    |  _ \ __ _ ___ _____      _____  _ __ __| | \ \   / /_ _ _   _| | |_ 
    | |_) / _` / __/ __\ \ /\ / / _ \| '__/ _` |  \ \ / / _` | | | | | __|
    |  __/ (_| \__ \__ \\ V  V / (_) | | | (_| |   \ V / (_| | |_| | | |_ 
    |_|   \__,_|___/___/ \_/\_/ \___/|_|  \__,_|    \_/ \__,_|\__,_|_|\__|""")

    print("A Place to store your passwords!!\n")

    def menu():
        print("""1. Enter Data
    2. View Data
    3. View All Saved Sites/Apps
    4. Clear All
    5. Exit""")

    def encrypt():
        w=input(f"PyOS:/home/apps/{username}/password_vault/name> ")
        u=input(f"PyOS:/home/apps/{username}/password_vault/username> ")
        p=input(f"PyOS:/home/apps/{username}/password_vault/password> ")
        l=[w,u,p]
        key=1
        for element in l:
            encrypted_data=''
            for letter in element:
                asci=(32+((ord(letter)-32+key)%95))
                encrypted_data+=chr(asci)
            with open(path+f"\\{APP_PATH}\\vault.txt","a") as file:
                file.write(encrypted_data+"\n")
            with open(path+f"\\{APP_PATH}\\backup.bin","ab") as file:
                file.write((encrypted_data+"\n").encode('utf-8'))
            key+=1
        print("\nEncrypted and saved successfully\n")
    def decrypt(i,key):
        decrypted_data=''
        for letter in i:
            if letter.strip() == '':
                continue
            asci=(32+((ord(letter)-32-key)%95))
            decrypted_data+=chr(asci)
        return decrypted_data
    def find():
        site=input("Enter site/app name: ")
        try:
            with open(path+f"\\{APP_PATH}\\vault.txt","r") as file:
                lines=file.readlines()
                count=0
                flag=False
                while count<len(lines):
                    dd=decrypt(lines[count].replace("\n",""),1)
                    if dd==site:
                        flag=True
                        print("\nData Found!!")
                        print("Site/app:",dd)
                        print("Username:",decrypt(lines[count+1].replace("\n",""),2))
                        print("Password:",decrypt(lines[count+2].replace("\n",""),3),"\n")
                        break
                    count+=3
                if not flag:
                    print("Sorry no data found with the name!!!")
        except FileNotFoundError:
            try:
                with open(path+f"\\{APP_PATH}\\backup.bin","rb") as file:
                    text=file.read().decode('utf-8')
                    lines=text.split("\n")
                    count=0
                    flag=False
                    while count<len(lines):
                        dd=decrypt(lines[count],1)
                        if dd==site:
                            flag=True
                            print("Data Found!!")
                            print("Site/app:",dd)
                            print("Username:",decrypt(lines[count+1],2))
                            print("Password:",decrypt(lines[count+2],3))
                            break
                        count+=3
                    if not flag:
                        print("Sorry no data found with the name!!!")
            except FileNotFoundError:
                print("Sorry there is NO DATA!!")
            except Exception:
                print("Something went wrong!!")
        except Exception:
            print("Something went wrong!!")

    def view():
        try:
            with open(path+f"\\{APP_PATH}\\vault.txt") as file:
                lines=[line.strip() for line in file.readlines() if line.strip()]
                count=0
                while count<len(lines):
                    dd=decrypt(lines[count].replace("\n",""),1)
                    print(dd)
                    count+=3
                print()
        except FileNotFoundError:
            try:
                with open(path+f"\\{APP_PATH}\\backup.bin") as file:
                    text=file.read().decode('utf-8')
                    lines=text.split("\n")
                    count=0
                    while count<len(lines):
                        dd=decrypt(lines[count],1)
                        print(dd)
                        count+=3
            except FileNotFoundError:
                print("Sorry NO DATA to view!!")
            except Exception:
                print("Something went wrong!!")
        except Exception:
            print("Something went wrong!!!")

    def clearall():
        try:
            open("vault.txt","w").close()
            open("backup.bin","wb").close()
        except FileNotFoundError:
            print("No data exist!!")
        except Exception as PVError:
            print(f"Something went wrong while clearing DATA!!: {PVError}\n")
        else:
            print("DATA CLEARED!!\n")
    if __name__=="__main__":
        while True:
            menu()
            try:
                op=int(input(f"PyOS:/home/apps/{username}/password_vault/option> "))
            except ValueError:
                print("Invalid DataType!!")
            else:
                if op==1:
                    encrypt()
                elif op==2:
                    find()
                elif op==3:
                    view()
                elif op==4:
                    clearall()
                elif op==5:
                    print("Exiting. ",end="")
                    for _ in range(2):
                        time.sleep(0.5)
                        print(". ",end="")
                    print()
                    break
                else:
                    print("Invalid option!!")

import os
import time

APP_PATH="notes"

def main(username,path):
    try:
        if not (os.path.isdir(f"{path}\\{APP_PATH}")):
            os.mkdir(f"{path}\\{APP_PATH}")
    except Exception as nerror:
        print(f"NOTES ERROR: {nerror}")

    print()
    print(r""" _   _ _____ _____ _____ _____ 
| \ | |  _  |_   _|  ___/  ___|
|  \| | | | | | | | |__ \ `--. 
| . ` | | | | | | |  __| `--. \
| |\  \ \_/ / | | | |___/\__/ /
\_| \_/\___/  \_/ \____/\____/ """)    

    def add_notes():
        note=input(f"PyOS:/home/{username}/apps/notes/add-note> ")
        try:
            f1=open(path+f"\\{APP_PATH}\\notes.txt","a")
            f1.write(note+"\n")
            f1.close()
        except Exception as ADDNOTEError:
            print(f"ERROR ADDING NOTE: {ADDNOTEError}")
        print("Note Added Successfully")
    def view_notes():
        try:
            f1=open(path+f"\\{APP_PATH}\\notes.txt","r")
            notes=f1.readlines()
            f1.close()
            if not notes:
                print("NO NOTES ARE AVAILABLE!")
            else:
                for serial_no,note in enumerate(notes):
                    note=note.strip()
                    print(f"Note {serial_no+1} : {note}")
        except FileNotFoundError:
            print("FNFE: NO NOTES ARE AVAILABLE!")
        except Exception as NotesError:
            print(f"ERROR: {NotesError}")
        
    def delete_notes():
        try:
            n=int(input(f"PyOS:/home/{username}/apps/notes/line-no> "))
            f1=open(path+f"\\{APP_PATH}\\notes.txt","r")
            notes=f1.readlines()
            f1.close()
            if 1<=n<=len(notes):
                del_txt=notes[n-1].strip()
                with open(path+f"\\{APP_PATH}\\notes.txt","w") as file:
                    for note in notes:
                        if note.strip() != del_txt:
                            file.write(note)
                print("NOTE DELETED")
            else:
                print("INVALID NOTE NUMBER")
        except ValueError:
            print("ERROR: Enter a number!")
        except FileNotFoundError:
            print("ERROR: Notes file doesn't exist")
        except Exception as NotesError:
            print(f"ERROR: {NotesError}")
        
    def menu():
        print("\n1.ADD A NOTE")
        print("2.VIEW ALL NOTES")
        print("3.DELETE A NOTE")
        print("4.EXIT")

#MAIN LOOP
    while True:
        menu()
        try:
            choice=int(input(f"\nPyOS:/home/{username}/apps/notes/option> "))
            if choice==1:
                add_notes()
            elif choice==2:
                view_notes()
            elif choice==3:
                delete_notes()
            elif choice==4:
                print("Exiting. ",end="")
                for _ in range(2):
                    time.sleep(0.5)
                    print(". ",end="",flush=True)
                print()
                return "Exited!"
            else:
                print("ERROR: INVALID CHOICE")
        except ValueError:
            print("Enter only Numbers!!")
        except Exception as APPError:
            print(f"App Error: {APPError}")
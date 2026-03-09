def add_notes():
    note=input("\nPyOS:/home/user/apps/notes/note> ")
    f1=open("notes.txt","a")
    f1.write(note+"\n")
    f1.close()
    print("Note Added Successfully")
def view_notes():
    try:
        f1=open("notes.txt","r")
        notes=f1.readlines()
        f1.close()
        if not notes:
            print("NOTES EMPTY")
        else:
            for serial_no,note in enumerate(notes):
                note.replace("\n","")
                print(f"Note {serial_no+1} : {note}")
    except FileNotFoundError:
        print("ERROR: Notes file doesn't exist")
    except Exception as NotesError:
        print("ERROR:",NotesError)
    
def delete_notes():
    try:
        n=int(input("\nPyOS:/home/user/apps/notes/line_no> "))
        f1=open("notes.txt","r")
        notes=f1.readlines()
        if 1<=n<=len(notes):
             print("NOTE DELETED")
             notes.pop(n-1)
        else:
             print("INVALID NOTE NUMBER")
    except ValueError:
        print("ERROR: Enter a number!")
    except FileNotFoundError:
        print("ERROR: Notes file does'nt exist")
    except Exception as NotesError:
        print("ERROR:",NotesError)
    
def menu():
    print("1.ADD NOTES")
    print("2.VIEW NOTES")
    print("3.DELETE NOTE")
    print("4.EXIT")
while True:
    menu()
    choice=int(input("\nPyOS:/home/user/apps/notes/option> "))
    if choice==1:
        add_notes()
    elif choice==2:
        view_notes()
    elif choice==3:
        delete_notes()
    elif choice==4:
        print("EXITING THE APP")
        break
    else:
        print("ERROR: INVALID CHOICE")

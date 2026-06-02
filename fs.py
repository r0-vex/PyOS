from logger import Logger
import os
import json
from datetime import datetime 
import security
import shutil

user_log = Logger.system()

def user_log_init(username):
    global user_log
    user_log=Logger.user(username)

class ExtNotAllowed(Exception):
    pass

class UserLogger:
    @staticmethod
    def action(action_type,details):
        user_log.info(f"[{action_type}] {details}")
    @staticmethod
    def error(details):
        user_log.error(details)
    @staticmethod
    def warning(details):
        user_log.warning(details)

PyOS_path=os.getcwd()
whitelist_ext=[".txt",".json",".csv",".py",".bin"]
SYSTEM_ROLE="PyOS"

sys_log=Logger.system()

def resolve_virtual_path(current, path):
    path = path.replace("\\", "/")
    if path.startswith("/"):
        # virtual root path
        return path[1:]
    else:
        return os.path.join(current,path)
        
class file:
        
    def change_dir(current,path,current_role,current_user):
        try:
            # home
            if path == "/":
                return os.path.join("users",current_user,"home")
            # current dir
            if path == ".":
                return current
            # back
            if path == "..":
                parent = os.path.dirname(current)
                # prevent escaping user root
                user_root = os.path.join("users",current_user)
                if os.path.commonpath([parent,user_root]) != user_root:
                    return user_root
                return parent
            # normal dir
            new_path = resolve_virtual_path(current,path)
            safe = security.AccessControl.authorize(new_path,current_role,current_user)
            if safe is None:
                return current
            if not os.path.isdir(safe):
                print("Directory Not Found")
                return current
            return new_path
        except Exception as DirError:
            sys_log.error(str(DirError))
            return current
        
    def list_dir(path,current_role,current_user):
        try:
            safe = security.AccessControl.authorize(path,current_role,current_user)
            if safe is None:
                return
            return os.listdir(safe)
        except Exception as FSError:
            sys_log.error(str(FSError))
            return None

    def create_dir(path,current_role,current_user):
        try:
            safe = security.AccessControl.authorize(path,current_role,current_user,"write")
            if safe is None:
                return
            if not (os.path.exists(safe)):
                os.mkdir(safe)
                if current_role!=SYSTEM_ROLE:
                    print(os.path.basename(path)+" Directory Created")
                sys_log.info(safe+" Directory Created")
                UserLogger.action("CREATE DIR",path)
            else:
                print("Directory Already Exists")
        except FileExistsError:
            sys_log.error("ERROR 2a: Directory Exists")
        except Exception as FileCreationError:
            sys_log.error("ERROR 2b: "+str(FileCreationError))

    def cr_file(path,current_role,current_user):
        try:
            safe=security.AccessControl.authorize(path,current_role,current_user,"write")
            if safe is None:
                return
            if "." not in os.path.basename(safe):
                safe += ".txt"
            if not (os.path.exists(safe)):
                if safe.endswith(tuple(whitelist_ext)):
                    open(safe,"w").close()
                    print(os.path.basename(safe)+" File Created")
                    sys_log.info(safe+" File Created")
                    UserLogger.action("CREATE",os.path.basename(safe))
                else:
                    raise ExtNotAllowed
            else:
                print("File Already Exists")
        except FileExistsError:
            sys_log.error("ERROR 2d: File Exists")
        except ExtNotAllowed:
            sys_log.error("Error 2e: Extension not allowed!")
        except Exception as FileCreationError:
            sys_log.error("ERROR 2f: "+str(FileCreationError))

    def remove_dir(path,current_role,current_user):
        try:
            safe = security.AccessControl.authorize(path,current_role,current_user,"delete")
            if safe is None:
                return
            if not (os.path.exists(safe)):
                sys_log.error("No such directory exists.")
                return
            else:
                os.rmdir(safe)
                sys_log.info(f"{safe} removed successfully")
                UserLogger.action("DELETE DIR",path)
                print("Successfully removed!")
        except OSError:
            sys_log.error("Non Empty Directory!")
        except Exception as FSError:
            sys_log.error("Unable to perform action!!"+str(FSError))

    def remove_file(path,current_role,current_user):
        try:
            safe = security.AccessControl.authorize(path,current_role,current_user,"delete")
            if safe is None:
                return
            if not (os.path.exists(safe)):
                sys_log.error("No such file exists.")
                return
            else:
                os.remove(safe)
                sys_log.info(f"{safe} removed successfully")
                UserLogger.action("DELETE",path)
                print("Successfully removed!")
        except IsADirectoryError:
            sys_log.error(f"{safe} is a directory!")
        except Exception as FSError:
            sys_log.error("Unable to perform action!!"+str(FSError))
    
    def readf(path,mode,current_role,current_user):
        try:
            safe=security.AccessControl.authorize(path,current_role,current_user)
            if safe is None:
                return
            if not os.path.exists(safe):
                sys_log.error("File not found")
                return
            if not os.path.isfile(safe):
                sys_log.error("Not a file")
                return
            if not safe.endswith(".txt"):
                sys_log.error("Unsupported format")
                return
            with open(safe) as temp_reader:
                temp_py_reader=temp_reader.readlines()
            if mode=="-l":
                for count,line in enumerate(temp_py_reader):
                    print(f"{count+1} | {line}",end='')
                print()
                return
            for line in temp_py_reader:
                print(line,end='')
            print()
            UserLogger.action("READ",path)
            return
        except Exception as ReadError:
            sys_log.error("ERROR 2g: "+str(ReadError))

    def writef(path,content,current_role,current_user):
        try:
            safe=security.AccessControl.authorize(path,current_role,current_user,"write")
            if safe is None:
                return
            if os.path.isfile(safe) and safe.endswith(tuple(whitelist_ext)):
                line=""
                for w_no,word in enumerate(content):
                    if w_no!=len(content)-1:
                        line+=(word+" ")
                        continue
                    line+=word
                with open(safe,"a") as w_file:
                    w_file.write(line + "\n")
                UserLogger.action("WRITE",path)
        except IsADirectoryError:
            sys_log.error(f"{safe} is a directory!")
        except Exception as WriteError:
            sys_log.error("Unable to perform action!!"+str(WriteError))
    def editf(path,current_role,current_user):
        try:
            safe = security.AccessControl.authorize(path,current_role,current_user,"write")
            if safe is None:
                return
            if os.path.isdir(safe):
                print("Given arg is a Directory")
                return
            new_file=False
            if not os.path.isfile(safe):
                if not safe.endswith(".bin"):
                    open(safe,"w").close()
                    sys_log.info(f"{safe} file created")
                    new_file=True
                else:
                    print("Un-supported file format")
                    return
            buffer=[]
            if not new_file:
                with open(safe,"r") as reader:
                    buffer = reader.readlines()
            os.system("cls" if os.name=="nt" else "clear")
            if new_file:
                print(f"{os.path.basename(safe)} [NEW FILE]")
            else:
                print(f"{os.path.basename(safe)}")
            print("\nPyOS Nano Editor")
            print("Type ':wq' to save and exit")
            print("Type ':q' to exit\n")
            if not new_file:
                for no,line in enumerate(buffer):
                    print(f"{no+1} | {line}",end="")
            while True:
                line = input("> ")
                if line.strip() == ":wq":
                    with open(safe,"w") as writer:
                        writer.writelines(buffer)
                    print("Saved.")
                    UserLogger.action("EDIT",path)
                    return
                if line.strip() == ":q":
                    print("Exited.")
                    return
                buffer.append(line + "\n")
        except Exception as EditError:
            sys_log.error("ERROR EDIT: "+ str(EditError))
        
    def rename(path, new_name, current_role, current_user):
        try:
            safe=security.AccessControl.authorize(path,current_role,current_user,"write")
            if safe is None:
                return
            if "/" in new_name or "\\" in new_name:
                print("Invalid filename")
                return
            new_safe=os.path.join(os.path.dirname(safe),new_name)
            if not security.AccessControl.check_permission(new_safe,current_role,current_user,"write"):
                return
            if not os.path.exists(safe):
                sys_log.error("Source Path doesn't exists")
                return
            if os.path.exists(new_safe):
                sys_log.error("Destination Name Already exists")
                return
            is_file=os.path.isfile(safe)
            os.rename(safe,new_safe)
            print(f"{'File ' if is_file else 'Directory '}renamed")
            old_base=os.path.basename(safe)
            new_base=os.path.basename(new_safe)
            UserLogger.action("RENAME",f"{'File ' if is_file else 'Directory '} {old_base} renamed to {new_base}")
        except Exception as RenameError:
            sys_log.error("ERROR 2h: "+str(RenameError))
            return
        
    def copy(src, dst, current_role, current_user):
        try:
            src_safe=security.AccessControl.authorize(src,current_role,current_user,"read")
            dst_safe=security.AccessControl.authorize(dst,current_role,current_user,"write")
            if src_safe is None or dst_safe is None:
                return
            if not os.path.exists(src_safe):
                sys_log.error("Source file doesn't exists")
                return
            if os.path.isdir(src_safe):
                sys_log.error("Directory can't be copied")
                return
            if src_safe == dst_safe:
                sys_log.error("Source and Destination are same")
                return
            if os.path.exists(dst_safe):
                UserLogger.warning("Destination already exists")
                ask=input("Do you want to overwrite it? (Y/N)=> ")
                if ask.lower()!="y":
                    return
            shutil.copy2(src_safe,dst_safe)
            print(f"{os.path.basename(src_safe)} copied successfully")
            UserLogger.action("COPY",f"{src} copied to {dst}")
        except IOError:
            sys_log.error("Destination is non writable")
        except IsADirectoryError:
            sys_log.error("Directory can't be copied")
        except Exception as CopyError:
            sys_log.error("ERROR 2i: "+str(CopyError))
            
    def move(src,dst,current_role,current_user):
        try:
            src_safe=security.AccessControl.authorize(src,current_role,current_user,"write")
            dst_safe=security.AccessControl.authorize(dst,current_role,current_user,"write")
            if src_safe is None or dst_safe is None:
                return
            if not os.path.exists(src_safe):
                sys_log.error("Source doesn't exists")
                return
            if src_safe == dst_safe:
                sys_log.error("Source and Destination are same")
                return
            if os.path.exists(dst_safe):
                UserLogger.warning("Destination already exists")
                ask=input("Do you want to overwrite it? (Y/N)=> ")
                if ask.lower()!="y":
                    return
            shutil.move(src_safe,dst_safe)
            print(f"{os.path.basename(dst_safe)} moved successfully")
            UserLogger.action("MOVE",f"{src} moved to {dst}")
        except Exception as MoveError:
            sys_log.error("ERROR 2j: "+str(MoveError))

class user_files_creation():
    def create_user_files(username,mode,is_admin=False):
        try:
            user_path=os.path.join(PyOS_path,"users",username)
            backup_template_path=os.path.join(PyOS_path,"system","backup","configs")
            system_path=os.path.join(user_path,"system")
            file.create_dir(os.path.join("users",username),current_role=mode,current_user=username)
            file.create_dir(os.path.join("users",username,"home"),current_role=mode,current_user=username)
            file.create_dir(os.path.join("users",username,"system"),current_role=mode,current_user=username)
            file.create_dir(os.path.join("users",username,"apps"),current_role=mode,current_user=username)
            file.create_dir(os.path.join("system","backup","users",username),current_role=mode,current_user=username)
            curr_date_time=f"{datetime.now().strftime('%d %B %Y')} {datetime.now().strftime('%I:%M:%S %p')}"
            if not is_admin:
                with open(os.path.join(backup_template_path,"userconfig.json")) as user_settings:
                    loaded_user_config=json.loads(user_settings.read())
            else:
                with open(os.path.join(backup_template_path,"adminconfig.json")) as user_settings:
                    loaded_user_config=json.loads(user_settings.read())
            loaded_user_config["created_on"]=curr_date_time
            if not (os.path.isfile(os.path.join(system_path,"config.json"))):
                with open(os.path.join(system_path,"config.json"),"w") as user_config:
                    json.dump(loaded_user_config,user_config,indent=4)
                sys_log.info("config.json has been created for "+username)
            if not (os.path.isfile(os.path.join(system_path,"log.txt"))):
                open(os.path.join(system_path,"log.txt"),"w").close()
                sys_log.info("log.txt has been created for "+username)
        except Exception as UserFileCreationError:
            sys_log.error("ERROR 2c: "+str(UserFileCreationError))

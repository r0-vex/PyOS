import logging
import os
import json
from datetime import datetime

#PyOS->FILES(main.py,fs.py,commands.py,auth.py,security.py)
#PyOS->FOLDERS(system,users,apps)
#PyOS->apps->(app1,app2,...)
#PyOS->users->(user1,user2,...)
#PyOS->users->user1->user_files->(file1,file2,...)
#PyOS->users->user1->system->(config.json,log.txt)
#PyOS->system->(config.json,log.txt)/FOLDER(backup)
#PyOS->system->backup->(configs,os,users,logs)
#PyOS->system->backup->configs->users and admin config backups 
#PyOS->system->backup->os->os files backups
#PyOS->system->backup->users->users files backup
#PyOS->system->backup->logs->backup logs

PyOS_path=os.getcwd()
whitelist_ext=["txt","json","csv","py","bin"]

class log():
    def __init__(self,name,path,console_level=logging.WARNING, file_level=logging.DEBUG):

        self.logger=logging.getLogger(name) #setting name to logger
        self.logger.setLevel(logging.DEBUG)

        if self.logger.handlers:
            return
        
        console_handler=logging.StreamHandler() #setting consoler
        console_handler.setLevel(console_level)

        file_handler=logging.FileHandler(os.path.join(os.getcwd(),path),"a+",encoding="utf-8") #setting file handler
        file_handler.setLevel(file_level)

        formatter=logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s") #log format

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)  # setting format to handlers

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler) #setting handlers to logger

sys_log=log("System Log",os.path.join("system","log.txt")).logger

class file(log):
    def create_dir(path):
        try:
            if not (os.path.exists(os.path.join(os.getcwd(),path))):
                os.mkdir(os.path.join(os.getcwd(),path))
                sys_log.info(os.path.join(os.getcwd(),path)+" Directory Created")
        except FileExistsError:
            sys_log.error("ERROR 2a: Directory Exists")
        except Exception as FileCreationError:
            sys_log.error("ERROR 2b: "+str(FileCreationError))

    def remove_dir(path):
        try:
            parent=os.getcwd()
            if not (os.path.exists(parent+path)):
                sys_log.error("No such directory exists.")
                return
            else:
                os.rmdir(parent+path)
                sys_log.info(rf"{path} removed successfully")
                print("Successfully removed!")
        except Exception as FSError:
            sys_log.error("Unable to perform action!!"+str(FSError))

    def remove_file(path):
        try:
            parent=os.getcwd()
            if not (os.path.exists(parent+path)):
                sys_log.error("No such directory exists.")
                return
            else:
                os.remove(parent+path)
                sys_log.info(rf"{path} removed successfully")
                print("Successfully removed!")
        except Exception as FSError:
            sys_log.error("Unable to perform action!!"+str(FSError))
    
class user_files_creation():
    def create_user_files(username,mode="user"):
        try:
            user_path=os.path.join(os.getcwd(),"users",username)
            config_path=os.path.join(os.getcwd(),"system","backup","configs")
            system_path=os.path.join(user_path,"system")
            file.create_dir(os.path.join("users",username))
            file.create_dir(os.path.join("users",username,"system"))
            file.create_dir(os.path.join("users",username,"apps"))
            file.create_dir(os.path.join("system","backup","users",username))
            curr_date_time=f"{datetime.now().strftime('%d %B %Y')} {datetime.now().strftime('%I:%M:%S %p')}"
            if mode=="user":
                with open(os.path.join(config_path,"userconfig.json")) as user_settings:
                    loaded_user_config=json.loads(user_settings.read())
            else:
                with open(os.path.join(config_path,"adminconfig.json")) as user_settings:
                    loaded_user_config=json.loads(user_settings.read())
            loaded_user_config["created_on"]=curr_date_time
            if not (os.path.isfile(os.path.join(system_path,"config.json"))):
                with open(os.path.join(system_path,"config.json"),"w") as user_config:
                    user_config.write(json.dumps(loaded_user_config))
                sys_log.info("config.json has been created for "+username)
            if not (os.path.isfile(os.path.join(system_path,"log.txt"))):
                open(os.path.join(system_path,"log.txt"),"w").close()
                sys_log.info("log.txt has been created for "+username)
        except Exception as UserFileCreationError:
            sys_log.error("ERROR 2c: "+str(UserFileCreationError))

#the os checks for lock if locked asks for admin password to unlock it
#then login page opens
#intially the user logs in
#if user types logsout
#then login page reappears with resetting the auth.login.var_name

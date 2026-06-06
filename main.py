import os
import time
import json
import auth,fs,commands
import sys
from logger import Logger

SYSTEM_ROLE="PyOS"

boot_start=time.time() #boot time
sys_log=Logger.system()
try:
    config_path=os.path.join(os.getcwd(),"system","config.json")
    with open(config_path) as ver_conf:
        temp_dict=json.loads(ver_conf.read())
        version_no=temp_dict["version"]
        version_name=temp_dict["version_name"]
        del temp_dict
except FileNotFoundError:
    sys_log.error("ERROR 0: Unable to load config file")
except Exception as BootError:
    sys_log.error("ERROR 0: Unable to load PyOS version "+str(BootError))

sys_log.info("Boot Started")

try:
    curr_date_time=f"{commands._date_(None)} {commands._time_(["--12"])[-1:-12:-1][::-1]}"
except:
    sys_log.error("Unable to load date and time")
     
os.system(f"title PyOS {version_no}")
time.sleep(1)
commands.clear(None)

print(r"""
  ____         ___  ____          _____  ___  
 |  _ \ _   _ / _ \/ ___|  __   _|___ / / _ \ 
 | |_) | | | | | | \___ \  \ \ / / |_ \| | | |
 |  __/| |_| | |_| |___) |  \ V / ___) | |_| |
 |_|    \__, |\___/|____/    \_/ |____(_)___/ 
        |___/                                 
""")

time.sleep(1)
print(f"Booting PyOS {version_no} . ",end="")
for _ in range(5):
    time.sleep(0.5)
    print(". ",end="",flush=True)
print()

print("Checking Python Version. ",end="")
#checking python version
try:
    required=(3,10)
    current=sys.version_info[:2]
    if current<required:
        print("FAILED")
        sys_log.critical(f"Python {required[0]}.{required[1]}+ required")
        time.sleep(2)
        sys.exit()
except Exception as VersionError:
    sys_log.error("ERROR 0p: "+str(VersionError))
for _ in range(3):
    time.sleep(0.5)
    print(". ",end="",flush=True)
print(f"OK ({sys.version.split()[0]})")

#checking config file
try:
    if not (os.path.isfile(config_path)):
        print("System Config Existance: False")
        raise FileNotFoundError
    print("System Config Existance: True")
    time.sleep(2)
    print("Loading settings from system config. ",end="")
#loading config file
    with open(config_path) as boot_sys_config: 
        boot_py_config=json.loads(boot_sys_config.read())
        sys_log.info("System Config Loaded Successfully in main.py")
    boot_flag=boot_py_config["boot_flag"]
    for _ in range(3):
        time.sleep(0.5)
        print(". ",end="",flush=True)
    print("OK")
#os files
    time.sleep(3)
    print("Loading kernel modules. ",end="")      
    required_files=["fs.py","commands.py","auth.py","security.py","logger.py"]
    for file in required_files:
        if not (os.path.isfile(os.path.join(os.getcwd(),file))):
            print(f"{file}: Not Found")
            #troubleshoot
            raise FileNotFoundError
    if not boot_flag:
        if not (os.path.isdir(os.path.join(os.getcwd(),"users"))):
            raise FileNotFoundError
    else:
        fs.file.create_dir("users",SYSTEM_ROLE,None)
        fs.file.create_dir(os.path.join("system","backup","users"),SYSTEM_ROLE,None)
    sys_log.info("OS files loaded.")
    for _ in range(3):
        time.sleep(0.5)
        print(". ",end="",flush=True)
    print("OK")  
#loading apps
    print("Loading apps. ",end="",flush=True)
    if not (os.path.isdir(os.path.join(os.getcwd(),"apps"))):
         raise FileNotFoundError
    apps_list= [app for app in os.listdir(os.path.join(os.getcwd(),"apps")) if app not in commands.blacklist_apps and app.endswith(".py")]
    boot_py_config["apps"]=apps_list
    with open(config_path,"w") as py_sys_config:
        json.dump(boot_py_config,py_sys_config,indent=4)
    for _ in range(3):
         time.sleep(0.5)
         print(". ",end="",flush=True)
    print("OK")
#trimming logs
    print("Detecting and Trimming System logs . . . ",end='')
    auto_trim,max_log=boot_py_config["auto_trim"],boot_py_config["max_log"]
    if auto_trim:
        path=os.path.join(os.getcwd(),"system","log.txt")
        log_flag=Logger.trim_log(path,max_log,sys_log)
        if log_flag:
            print("OK")
        else:
            print("SKIPPED")
    else:
        print("SKIPPED")
except FileNotFoundError:
    sys_log.critical("ERROR 0: Unable to boot")
    sys.exit()
except Exception as BootError:
    sys_log.critical("ERROR 0a: "+str(BootError))
    sys.exit()

#boot successful
print("System ready. ",end="") 
for i in range(3):
    time.sleep(0.5)
    print(". ",end="",flush=True)

print("\nBoot Successful....")
sys_log.info("Boot Successful....")

boot_end=time.time() #boot time
print(f"Boot Time: {boot_end-boot_start:.2f}s")

#MAIN OS
if __name__=="__main__":
    while True:
        try:

            with open(os.path.join(os.getcwd(),"system","config.json")) as file:
                boot_sys_config=json.loads(file.read())
                boot_flag=boot_sys_config["boot_flag"]

            if boot_flag:
                if not auth.account_creation.admin_create():
                    sys_log.warning("Admin hasn't created!")
                    print("Shutting down. ",end="")
                    sys_log.info("OS Shutdown Executed!")
                    for _ in range(5):
                        time.sleep(0.7)
                        print(". ",end="",flush=True)
                    sys.exit(0)
                    break
                with open(config_path) as py_sys_config:
                    py_config=json.loads(py_sys_config.read())
                py_config["booted_on"]=curr_date_time
                py_config["boot_flag"]=False
                with open(config_path,"w") as py_sys_config:
                    json.dump(py_config,py_sys_config,indent=4)
                continue
            
            print("\nLOGIN\n")
            auth.login.users_list()
            login_flag=auth.login.auth_login()
            
            if login_flag:
                curr_user=auth.login.current_user
                user_log=Logger.user(curr_user)
                with open(os.path.join(os.getcwd(),auth.login.user_dir,"system","config.json")) as load_user_config:
                    user_config=json.loads(load_user_config.read())
                    os.system(user_config["theme"])
                    user_auto_trim,user_max_log=user_config["auto_trim"],user_config["max_log"]
                    if user_auto_trim:
                        path=os.path.join(os.getcwd(),"users",curr_user,"system","log.txt")
                        Logger.trim_log(path,user_max_log,user_log)
                if auth.login.current_user and auth.login.current_role!="admin":
                    locked=user_config["locked"]
                    lock=user_config["lock_until"]
                else:
                    lock,locked=0,False
                if time.time() < lock or locked:
                    print(f"\nRemaining Time: {(lock-time.time())//60}m")
                    user_log.critical("OS Locked!")
                    sys_log.critical(f"{auth.login.current_user} OS Locked!")
                    print("Use Admin Password to Remove lock")
                    option=input("Y/N> ")
                    if option.lower()=="y":
                        login_flag=auth.login.auth_login()
                        if login_flag and auth.login.current_role=="admin":
                            user_config["lock_until"]=0
                            user_config["locked"]=False
                            with open(os.path.join(os.getcwd(),"users",curr_user,"system","config.json"),"w") as py_user_config:
                                json.dump(user_config,py_user_config,indent=4)
                            sys_log.info(curr_user+" lock removed!")
                            user_log.info("OS Lock Removed!")
                            auth.login.current_user=auth.login.current_role=auth.login.current_dir=auth.login.user_dir=None
                            print("Lock Removed!")
                            continue
                        else:
                            print("OS Shutting down. ",end="")
                            user_log.info("Logged Out by OS")
                            sys_log.info("OS Shutdown Executed!")
                            for _ in range(5):
                                time.sleep(0.7)
                                print(". ",end="",flush=True)
                            sys.exit(0)
                else:
                    print("Logging in. ",end="")
                    for _ in range(3):
                        time.sleep(0.7)
                        print(". ",end="",flush=True)
                    user_log.info("Logged in...")
                    sys_log.info(auth.login.current_user+" logged in...")
                    print("\nLogin Successfull.")
                    commands.clear(None)
                    print(f"PyOS [version {version_name}]\n(info) Python based kernel os simulator.")
                    fs.user_log_init(auth.login.current_user)
                    commands.assign()
            #shell loop 
                    while True:
                        display_path = auth.login.current_dir.replace("\\","/")
                        cmd=input(f"PyOS:/{display_path}> ").strip()
                        if cmd.lower()=="shutdown":
                            print("Shutting down. ",end="")
                            user_log.info("Logged Out!")
                            sys_log.info("Shutdown Executed!")
                            for _ in range(5):
                                time.sleep(0.7)
                                print(". ",end="",flush=True)
                            sys.exit(0)
                        elif cmd.lower()=="logout":
                            print("Logging out. ",end="")
                            for _ in range(3):
                                time.sleep(0.7)
                                print(". ",end="",flush=True)
                            commands.execute(cmd.lower())
                            sys_log.info(curr_user+" Logged Out...")
                            commands.clear(None)
                            break
                        commands.execute(cmd)
                    if cmd.lower()=="shutdown":
                        sys.exit(0)
            else:
                if auth.login.current_user and auth.login.current_user != boot_sys_config["admin"]:
                    user_log=Logger.user(auth.login.current_user)
                    with open(os.path.join(os.getcwd(),"users",auth.login.current_user,"system","config.json")) as load_user_config:
                        user_config=json.loads(load_user_config.read())
                    user_config["lock_until"]=time.time()+300
                    user_config["locked"]=True
                    with open(os.path.join(os.getcwd(),"users",auth.login.current_user,"system","config.json"),"w") as py_user_config:
                        json.dump(user_config,py_user_config,indent=4)
                    user_log.critical("OS set to Locked!")
                    sys_log.critical(auth.login.current_user+" OS set to Locked!")
                print("Shutting down. ",end="")
                for _ in range(5):
                    time.sleep(0.7)
                    print(". ",end="",flush=True)
                break
        except FileNotFoundError:
            sys_log.critical(f"{auth.login.current_user} Config Not Found")
            user_log=Logger.user(auth.login.current_user)
            user_log.critical("User Config Not Found")
        except KeyboardInterrupt:
            print("Shutting down. ",end="")
            sys_log.info("Shutdown Executed!")
            for _ in range(5):
                time.sleep(0.7)
                print(". ",end="",flush=True)
            sys.exit(0)
        except Exception as BootError:
            sys_log.error("ERROR 0b: "+str(BootError))
import os
import time
import json
import auth,fs,commands
import sys

boot_start=time.time() #boot time

fs.log.logger.info("Boot Started")
os.system("title PyOS v2.0")
time.sleep(1)

print(r"""  _____        ____   _____        ___    ___  
 |  __ \      / __ \ / ____|      |__ \  / _ \ 
 | |__) |   _| |  | | (___   __   __ ) || | | |
 |  ___/ | | | |  | |\___ \  \ \ / // / | | | |
 | |   | |_| | |__| |____) |  \ V // /_ | |_| |
 |_|    \__, |\____/|_____/    \_/|____(_)___/ 
         __/ |                                 
        |___/                                  """)

time.sleep(1)
print("Booting PyOS v2.0 . ",end="")
for _ in range(5):
    time.sleep(0.5)
    print(". ",end="",flush=True)
print()

print("Checking Python Version. ",end="")
#checking python version
try:
    config_path=os.getcwd()+r"\system\config.json"
    with open(config_path) as py_sys_config: 
        py_config=json.loads(py_sys_config.read())
        version=sys.version.split()[0]
        py_config["python_version"]=version
    with open(config_path,"w") as py_sys_config:
        py_sys_config.write(json.dumps(py_config))
except FileNotFoundError:
                fs.log.logger.error("ERROR 0p: Unable to find version")
except Exception as VersionError:
                fs.log.logger.error("ERROR 0p: "+str(VersionError))
for _ in range(5):
    time.sleep(0.5)
    print(". ",end="",flush=True)
print()
fs.log.logger
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
        fs.log.logger.info("System Config Loaded Successfilly in main.py")
    lock=boot_py_config["lock_until"]
    locked=boot_py_config["locked"]
    boot_flag=boot_py_config["boot_flag"]
    os.system(boot_py_config["color"])
    for _ in range(8):
            time.sleep(0.5)
            print(". ",end="",flush=True)
    print()
#os files
    time.sleep(3)
    print("Loading kernel modules. ",end="")      
    required_files=["fs.py","commands.py","auth.py","security.py"]
    for file in required_files:
        if not (os.path.isfile(os.getcwd() + "\\" + file)):
            print(f"{file}: Not Found")
            raise FileNotFoundError
    if not boot_flag:
        if not (os.path.isdir(os.getcwd() + r"\users")):
            raise FileNotFoundError
    else:
        fs.file.create_dir(os.getcwd()+"\\users")
    fs.log.logger.info("OS files loaded.")
    for _ in range(8):
        time.sleep(0.5)
        print(". ",end="",flush=True)
    print()  
#loading apps
    print("Loading apps. ",end="",flush=True)
    if not (os.path.isdir(os.getcwd()+r"\apps")):
         raise FileNotFoundError
    boot_py_config["apps"]=os.listdir(os.getcwd()+r"\apps")
    with open(config_path,"w") as py_sys_config:
        py_sys_config.write(json.dumps(boot_py_config))
    for _ in range(3):
         time.sleep(0.5)
         print(". ",end="",flush=True)
    print()
except FileNotFoundError:
    fs.log.logger.critical("ERROR 0: Unable to boot")
    sys.exit()
except Exception as BootError:
    fs.log.logger.critical("ERROR 0a: "+str(BootError))
    sys.exit()

#boot successful
print("System ready. ",end="") 
for i in range(3):
    time.sleep(0.5)
    print(". ",end="",flush=True)

print("\nBoot Successful....")
fs.log.logger.info("Boot Successful....")

boot_end=time.time() #boot time
print(f"Boot Time: {boot_end-boot_start:.2f}s")

#MAIN OS
if __name__=="__main__":
    if boot_end>lock or not locked:
        try:
            with open(config_path,"w") as py_sys_config:
                    boot_py_config["locked"]=False
                    boot_py_config["lock_until"]=0
                    py_sys_config.write(json.dumps(boot_py_config))

            if boot_flag:
                auth.account_creation.admin_create()

            print("\nLOGIN\n")
            auth.login.users_list()
            login_flag=auth.login.auth_login()

            if login_flag:
                print("Logging in. ",end="")
                for _ in range(3):
                    time.sleep(0.7)
                    print(". ",end="",flush=True)
                print("\nLogin Successfull.")
                os.system("cls")
                print("PyOS [version 2.0.00]\n(info) Python based kernel os.")
    #Shell loop
                while True:
                    cmd=input(f"PyOS:/home/{auth.login.current_user}> ").strip()
                    if cmd.lower()=="shutdown":
                        print("Shutting down. ",end="")
                        fs.log.logger.info("Shutdown Executed!")
                        for _ in range(5):
                            time.sleep(0.7)
                            print(". ",end="",flush=True)
                        break
                    commands.execute(cmd.lower())
            else:
                boot_py_config["lock_until"]=time.time()+300
                boot_py_config["locked"]=True
                with open(config_path,"w") as py_sys_config:
                    py_sys_config.write(json.dumps(boot_py_config))
                fs.log.logger.critical("OS Locked!")
        except Exception as BootError:
            fs.log.logger.error("ERROR 0b: "+str(BootError))
    else:
        print(f"\nRemaining Time: {(lock-boot_end)//60}m")
        fs.log.logger.critical("OS Locked!")
        print("Use Admin Password to Remove lock")
        option=input("Y/N> ")
        if option.lower()=="y":
            login_flag=auth.login.auth_login()
        else:
            fs.log.logger.critical("OS Locked!")
        
import auth,fs
from security import AccessControl
from logger import Logger
import os
import json
import random
import importlib
from datetime import datetime
import calendar
import time
import sys

boot_time=time.time()

APPS_DIR="apps"
blacklist_apps=["__pycache__","__init__.py"]

config_path=user_log=cmd_py_config=None

sys_log=Logger.system()
sys_config_path=os.path.join(os.getcwd(),"system","config.json")

class InvalidApp(Exception):
    pass

def get_user_log():
    if auth.login.current_user is None:
        return sys_log
    return Logger.user(auth.login.current_user)

def get_config_path():
    if auth.login.current_user is None:
        return os.path.join(os.getcwd(),"system","config.json")
    return os.path.join(os.getcwd(),auth.login.user_dir,"system","config.json")

def assign():
        global user_log,config_path,cmd_py_config
        user_log=get_user_log()
        config_path=get_config_path()
        cmd_py_config=load_data(None)

def load_data(args):
    global cmd_py_config
    try:
        with open(config_path) as cmd_config:
            cmd_py_config=json.loads(cmd_config.read())
    except FileNotFoundError:
        return sys_log.critical("ERROR 2: System Config Not Found")
    except Exception as CMDError:
        return sys_log.error("ERROR 2: "+str(CMDError))
    return cmd_py_config

def dump_data(args):
    try:
        with open(config_path,"w") as _sys_config:
            json.dump(cmd_py_config,_sys_config,indent=4)
    except FileNotFoundError:
        return sys_log.critical("ERROR 2: System Config Not Found")
    except Exception as CMDError:
        return sys_log.error("ERROR 2: "+str(CMDError))
    return "System config overwritten successfully"

def get_pyos_ver(value):
    try:
        if value=="version":
            flag="version"
        else:
            flag="version_name"
        with open(sys_config_path) as ver_conf:
            return json.loads(ver_conf.read())[flag]
    except FileNotFoundError:
        sys_log.error("ERROR 2: Unable to load config file")
    except Exception as PyOSVersionError:
        sys_log.error("ERROR 2: Unable to load PyOS version "+str(PyOSVersionError))

def screenfetch(args):
    if not args:
        return r""" ____         ___  ____  
|  _ \ _   _ / _ \/ ___| 
| |_) | | | | | | \___ \ 
|  __/| |_| | |_| |___) |
|_|    \__, |\___/|____/ 
       |___/             """
    
    if len(args)>0:
        if args[0]=="-v":
            return(r"""
  ____         ___  ____          _____  ___  
 |  _ \ _   _ / _ \/ ___|  __   _|___ / / _ \ 
 | |_) | | | | | | \___ \  \ \ / / |_ \| | | |
 |  __/| |_| | |_| |___) |  \ V / ___) | |_| |
 |_|    \__, |\___/|____/    \_/ |____(_)___/ 
        |___/                                 
""")

def whoami(args):
    return auth.login.current_user

def clear(args):
    CLEAR_CMD = "cls" if os.name=="nt" else "clear"
    os.system(CLEAR_CMD)
    return

def _date_(args):
    return datetime.now().strftime("%d %B %Y")

def _time_(args):
    if "--24" in args:
        return "24-hour Format: "+datetime.now().strftime("%H:%M:%S")
    return "12-hour Format: "+datetime.now().strftime("%I:%M:%S %p")

def _day_(args):
    return "It's "+datetime.now().strftime("%A")

def greet(args):
    return "Welcome "+whoami(args)

def help(args):
    print("Available Commands:-")
    for commands,commands_dict in cmds.items():
        if commands_dict["permission"]=="admin" and auth.login.current_role!="admin":
            continue
        print(commands)
    return " "

def echo(args):
    return " ".join(args)

def _calendar_(args):
    try:
        if args:
            year,month=int(args[0]),int(args[1])
            cal=calendar.TextCalendar(calendar.SUNDAY)
            month_calendar=cal.formatmonth(year,month)
            return month_calendar
    except IndexError:
        return
    except Exception as CalendarError:
        user_log.debug("Calendar Error: "+str(CalendarError))
        return
    year,month=int(datetime.now().strftime("%Y")),int(datetime.now().strftime("%m"))
    cal=calendar.TextCalendar(calendar.SUNDAY)
    month_calendar=cal.formatmonth(year,month)
    return month_calendar

def mood(args):
    moods=["shy\n(#^.^#)","excited\n(o_^)","productive\n\\(^-^)/","happy\n^-^","sad\n:-(","sleepy\n(-_-)zzz","bored\n:-o zz z z Z  Z"]
    return f"{cmd_py_config['pet_name']} is feeling "+random.choice(moods)

def quote(args):
    quotes=['“Talk is cheap. Show me the code.”',
            '“Programmer: A machine that turns coffee into code.”',
            '“It’s not a bug; it’s an undocumented feature.”',
            '“If, at first, you do not succeed, call it version 1.0.”',
            '“Software is like sex: it’s better when it’s free.”',
            '“Don’t comment bad code – rewrite it.”',
            '“Make it work, make it right, make it fast.”',
            '“Code is read much more often than it is written.”',
            '“Code is like humor. When you have to explain it, it’s bad.”',
            '“Before software can be reusable, it first has to be usable.”',
            '“Fix the cause, not the symptom.”',
            '“There is always one more bug to fix.”',
            '“Experience is the name everyone gives to their mistakes.”',
            '“Programming is learned by writing programs.”',
            '“In the beginner’s mind, there are many possibilities; in the expert’s mind, there are few.”',
            '“Confusion is part of programming.”',
            '“Truth can only be found in one place: the code.”',
            '“The computer was born to solve problems that did not exist before.”',
            '“Software comes from heaven when you have good hardware.”',
            '“Computers are fast; developers keep them slow.”',
            '“Great Softwares are like wine; it takes time to be good.”',
            '“If you can read this, thank a Software Developer.”',
            '“Pasting code from the internet into production code is like chewing gum found in the street.”',
            '“If the code doesn\'t bother you, don\'t bother it.”'
            ]
    return random.choice(quotes)

def sysinfo(args):
    print("System Information:-")
    print("-"*50)
    print(f"{'current user':<25}: {auth.login.current_user}")
    print(f"{'current user directory':<25}: {auth.login.user_dir}")
    print(f"{'current directory':<25}: {auth.login.current_dir}")
    print("-"*50)
    for title,info in cmd_py_config.items():
        if title=="theme":
               break
        text=title.replace("_"," ")
        print(f"{text:<25}: {info}")
    print("-"*50)
    return " "

def petname(args):
    if args:
        cmd_py_config["pet_name"]=" ".join(args)
        dump_data(args)
        user_log.info("Pet name set")
        return "Pet Name Set"
    cmd_py_config["pet_name"]=f"PyOS {get_pyos_ver('version')}"
    dump_data(args)
    return "Pet Name Re-Setted"

def whoareu(args):
    return "I'm "+cmd_py_config["pet_name"]

def roll(args):
    return random.randint(1,6)

def coin(args):
    return random.choice(["Head","Tail"])

def matrix(args):
    os.system("color a")
    try:
        while True:
            line=""
            for i in range(40):
                number=random.randint(0,1)
                line+=str(number)
            time.sleep(0.1)
            print(line,flush=True)
    except KeyboardInterrupt:
        os.system(cmd_py_config["theme"])
        return " "

def users(args):
    print("Users:-")
    auth.login.users_list()
    return " "

def reverse(args):
    text=" ".join(args)
    return text[::-1]

def add_user(args):
    return_val=auth.account_creation.user_create()
    if return_val:
        return "User Created Successfully"
    return "Unable to create user!"

def logout(args):
    sys_log.info(f"{auth.login.current_user} logged out")
    if user_log is not None:
        user_log.info("Logged Out")
    auth.login.current_user=auth.login.current_role=auth.login.current_dir=auth.login.user_dir=None
    os.system("color f")
    return "\nLogged Out!"

def apps(args):
    try:
        with open(sys_config_path) as sys_config:
            sys_py_config=json.loads(sys_config.read())
        apps_list=sys_py_config["apps"]
        if not apps_list:
            apps_list= [app for app in os.listdir(os.path.join(os.getcwd(),"apps")) if app not in blacklist_apps and app.endswith(".py")]
        print("Available Apps:-")
        for count,app_name in enumerate(apps_list):
            print(f"{count+1}. {app_name.replace(".py","").replace("_"," ").capitalize()}")
        return " "
    except FileNotFoundError:
        user_log.error("Unable to load System Config: NOT FOUND")
        return
    except Exception as CMDError:
        user_log.error("Error CMD: "+str(CMDError))
        return

def theme(args):
    themes = {
        "matrix": {"code": "0a","desc": "Classic hacker green"},
        "bloodmoon": {"code": "04","desc": "Dark red danger"},
        "ocean": {"code": "1b","desc": "Cool aqua shell"},
        "royal": {"code": "5f","desc": "Purple elite"},
        "ghost":{"code":"08","desc":"Dark Mode"},
        "sunset":{"code":"60","desc":"Sunset black theme"},
        "ice":{"code":"1f","desc":"Cold Blue White"},
        "lava":{"code":"40","desc":"Hot Lava Black"},
        "neon":{"code":"0d","desc":"Black Magenta Theme"},
        "default": {"code": "f","desc": "Classic PyOS"}
    }
    if not args:
        print("\nAvailable Themes:-\n")
        for name, desc in themes.items():
            print(f"{name.title():<12} : {desc['desc']}")
        theme=input(f"\nEnter Theme Name: ").lower()
    if args:
        theme = args[0].lower()
    if theme not in themes:
        return "Theme not found"
    selected = themes[theme]
    os.system(f"color {selected['code']}")
    print(f"\nPreviewing Theme: {theme.upper()}")
    confirm = input("Apply Theme? (y/n): ")
    if confirm.lower() != "y":
        os.system(cmd_py_config["theme"])
        return "Theme cancelled"
    # save theme
    cmd_py_config["theme"] = f"color {selected['code']}"
    dump_data(None)
    return f"{theme.title()} theme applied"

def cmd(args):
    return f"PyOS [version {get_pyos_ver("ver_name")}]\n(info) Python based kernel os simulator.\n"

def os_info(args):
    os_args={"name":"os_name",
               "version":"version",
               "admin":"admin",
               "inboot":"booted_on",
               "totalu":"allowed_users",
               "createu":"created_users",
               "maxlog":"max_log",
               "all":"all"}
    if not args:
        for value in os_args:
            if value=="all":
                continue
            print(f"{value.upper()}")
        return "\nUsage: os <argument>"

    if args[0] not in os_args:
        return "Argument Not Found"
    
    with open(sys_config_path) as sys_config:
        sys_py_config=json.loads(sys_config.read())
    
    if args[0] == "all":
        for arg,key in os_args.items():
            if arg=="all":
                continue
            print(f"{arg.capitalize():<10}: {sys_py_config[key]}")
        return "\nUsage: os <argument>"

    return sys_py_config[os_args[args[0]]]

def py_version(args):
    return cmd_py_config["python_version"]

def uptime(args):
    seconds=time.time()-boot_time
    return f"Up-time : {str(int(seconds//3600)).zfill(2)}:{str(int(seconds%3600)//60 ).zfill(2)}:{str(int(seconds%60)).zfill(2)}"

def run(args):
    if not args:
        return "Usage: run <appname>"
    
    app_name=args[0]
    app_path=os.path.join(APPS_DIR,app_name+".py")

    if not (os.path.isfile(app_path)):
        return user_log.error(f"App: {app_name} not found")
    
    try:
        if not app_name.replace("_","").isalnum():
            raise InvalidApp
        module=importlib.import_module(f"{APPS_DIR}.{app_name}")
        importlib.reload(module)
        if not hasattr(module,"main"):
            return user_log.error("App has no main()")
        
        return module.main(auth.login.current_user,os.path.join(os.getcwd(),auth.login.user_dir,APPS_DIR))
    except InvalidApp:
        user_log.error("Invalid App")
    except Exception as CMDError:
        return user_log.error("App crashed "+str(CMDError))

def restart(args):
    print("Saving session...")
    time.sleep(1)
    print("Stopping services...")
    time.sleep(1)
    sys_log.info("Restarted...")
    print("Restarting kernel...")
    time.sleep(1)
    print("Restarting PyOS. ",end="")
    user_log.info("Restarted...")
    logout(None)
    for _ in range(3):
        time.sleep(0.7)
        print(". ",end="",flush=True)
    os.system("start boot.bat")
    sys.exit(0)

def ls(args):
    data = fs.file.list_dir(auth.login.current_dir,current_role=auth.login.current_role,current_user=auth.login.current_user)
    if data is None:
        return
    if len(data)==0:
        return "Directory Empty"
    safe_dir = AccessControl.authorize(auth.login.current_dir,auth.login.current_role,auth.login.current_user)
    if safe_dir is None:
        return
    for item in data:
        full_path=os.path.join(safe_dir,item)
        if os.path.isdir(full_path):
            print(f"[DIR] {item}")
        else:
            print(f"[FILE] {item}")

def crdir(args):
    if not args:
        return "Usage: crdir <dirname>"
    target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
    fs.file.create_dir(target,current_role=auth.login.current_role,current_user=auth.login.current_user)

def cr(args):
    if not args:
        return "Usage: cr <filename.ext>"
    fs.file.cr_file(os.path.join(auth.login.current_dir,args[0]),current_role=auth.login.current_role,current_user=auth.login.current_user)
def deldir(args):
    if not args:
        return "Usage: deldir <dirname>"
    target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
    fs.file.remove_dir(target,current_role=auth.login.current_role,current_user=auth.login.current_user)

def remove(args):
    if not args:
        return "Usage: remove <filename>"
    target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
    fs.file.remove_file(target,current_role=auth.login.current_role,current_user=auth.login.current_user)

def sd(args):
    if not args:
        return auth.login.current_dir
    auth.login.current_dir=fs.file.change_dir(auth.login.current_dir,args[0],current_role=auth.login.current_role,current_user=auth.login.current_user)

def pwd(args):
    return auth.login.current_dir

def readf(args):
    if not args:
        return "Usage: readf <filename.txt> <args>"
    if len(args)==2:
        if args[1]=="-l":
            target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
            fs.file.readf(target,"-l",current_role=auth.login.current_role,current_user=auth.login.current_user)
            return
    target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
    fs.file.readf(target,None,current_role=auth.login.current_role,current_user=auth.login.current_user)

def writef(args):
    if not args:
        return "Usage: writef <filename.ext> <data to be appended>"
    if len(args)>1:
        target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
        fs.file.writef(target,args[1::],current_role=auth.login.current_role,current_user=auth.login.current_user)
        return
    return "Insufficent Arguments"

def editf(args):
    if not args:
        return "Usage: edit <filename.ext>"
    target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
    fs.file.editf(target,current_role=auth.login.current_role,current_user=auth.login.current_user)

def rename(args):
    if len(args)!=2:
        return "Usage: rename <old name> <new name>"
    target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
    fs.file.rename(target,args[1],current_role=auth.login.current_role,current_user=auth.login.current_user)

def copy(args):
    if len(args)!=2:
        return "Usuage: copy <source path> <destination path>"
    src_target=fs.resolve_virtual_path(auth.login.current_dir,args[0])
    des_target=fs.resolve_virtual_path(auth.login.current_dir,args[1])
    fs.file.copy(src_target,des_target,current_role=auth.login.current_role,current_user=auth.login.current_user)

def move(args):
    if len(args)!=2:
        return "Usage: move <source> <destination>"
    src_target = fs.resolve_virtual_path(auth.login.current_dir,args[0])
    dst_target = fs.resolve_virtual_path(auth.login.current_dir,args[1])
    fs.file.move(src_target,dst_target,current_role=auth.login.current_role,current_user=auth.login.current_user)

cmds={"whoami": {"func":whoami,"permission":"user"},
       "clear": {"func":clear,"permission":"user"},
       "date": {"func":_date_,"permission":"user"},
       "time": {"func":_time_,"permission":"user"},
       "day": {"func":_day_,"permission":"user"},
       "greet": {"func":greet,"permission":"user"},
       "help":{"func":help,"permission":"user"},
       "echo":{"func":echo,"permission":"user"},
       "cal":{"func":_calendar_,"permission":"user"},
       "shutdown":{"permission":"user"},
       "mood":{"func":mood,"permission":"user"},
       "quote":{"func":quote,"permission":"user"},
       "matrix":{"func":matrix,"permission":"user"},
       "sysinfo":{"func":sysinfo,"permission":"user"},
       "roll":{"func":roll,"permission":"user"},
       "coin":{"func":coin,"permission":"user"},
       "petname":{"func":petname,"permission":"user"},
       "whoareu":{"func":whoareu,"permission":"user"},
       "reverse":{"func":reverse,"permission":"user"},
       "uptime":{"func":uptime,"permission":"user"},
       "run":{"func":run,"permission":"user"},
       "users":{"func":users,"permission":"admin"},
       "adduser":{"func":add_user,"permission":"admin"},
       #"deluser":deluser, deletes user
       "ls":{"func":ls,"permission":"user"},
       "crdir":{"func":crdir,"permission":"user"},
       "sd":{"func":sd,"permission":"user"},
       "pwd":{"func":pwd,"permission":"user"},
       "deldir":{"func":deldir,"permission":"user"},
       "copy":{"func":copy,"permission":"user"},
       "move":{"func":move,"permission":"user"},
       "rename":{"func":rename,"permission":"user"},
       "del":{"func":remove,"permission":"user"},
       "cr":{"func":cr,"permission":"user"},
       "readf":{"func":readf,"permission":"user"},
       "writef":{"func":writef,"permission":"user"},
       "edit":{"func":editf,"permission":"user"},
       #"man":man, manual for a particular cmd
       #"search":search, searchs a word in a file
       #"count":count , counts the number of words/letters/lines in a txt file
       "theme":{"func":theme,"permission":"user"},
       #"lock":lock, locks the os for a certain period of time
       "logout":{"func":logout,"permission":"user"},
       "restart":{"func":restart,"permission":"user"},
       #reset os, resets the entire os only by admin
       #reset user, resets all the user profile without deleting user
       "pyver":{"func":py_version,"permission":"user"},
       "cmd":{"func":cmd,"permission":"user"},
       "os":{"func":os_info,"permission":"user"},
       "apps":{"func":apps,"permission":"user"},
       "screenfetch":{"func":screenfetch,"permission":"user"}
       }

def execute(cmd):

    if auth.login.current_user is None:
       print("Not logged in")
       return
    
    try:
        part=cmd.split()
        if not part:
            return
        command=part[0].lower()
        args=part[1:]
        if command in cmds:
            cmd_info=cmds[command]
            if cmd_info["permission"]=="admin" and auth.login.current_role!="admin":
                user_log.critical("Permission Denied!")
                return
            output=cmd_info["func"](args)
            if output is not None:
                print(output)
                user_log.info(f"cmd={cmd} Executed Successfully")
            """else:
                user_log.error("Invalid Command "+cmd)"""
        else:
            user_log.error("Command Not Found")
    except Exception as CMDError:
            user_log.critical("Error CMD: "+str(CMDError))

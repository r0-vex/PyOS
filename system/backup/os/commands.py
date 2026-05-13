import auth,fs
import os
import json
import random
import importlib
from datetime import datetime
import calendar
import time

boot_time=time.time()

APPS_DIR="apps"

config_path=user_log=cmd_py_config=None

sys_log=fs.log("System Log","\\system\\log.txt").logger
sys_config_path=f"{os.getcwd()}\\system\\config.json"

def get_user_log():
    if auth.login.current_user is None:
        return sys_log
    return fs.log(
        f"User: {auth.login.current_user}",
        f"\\users\\{auth.login.current_user}\\system\\log.txt"
    ).logger

def get_config_path():
    if auth.login.current_user is None:
        return os.getcwd()+"\\system\\config.json"
    return f"{os.getcwd()}\\users\\{auth.login.current_user}\\system\\config.json"

class assign:
    def __init__(self):
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
            _sys_config.write(json.dumps(cmd_py_config))
    except FileNotFoundError:
        return sys_log.critical("ERROR 2: System Config Not Found")
    except Exception as CMDError:
        return sys_log.error("ERROR 2: "+str(CMDError))
    return "System config overwritten successfully"

def whoami(args):
    return auth.login.current_user

def clear(args):
    os.system("cls")
    return " "

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
    return f"{cmd_py_config["pet_name"]} is feeling "+random.choice(moods)

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
    print("-"*40)
    print(f"{'current user':<20}: {auth.login.current_user}")
    print(f"{'current directory':<20}: \\users\\{auth.login.current_user}")
    print("-"*40)
    for title,info in cmd_py_config.items():
        if title=="color":
               break
        text=title.replace("_"," ")
        print(f"{text:<20}: {info}")
    print("-"*40)
    return " "

def petname(args):
    if args:
        cmd_py_config["pet_name"]=" ".join(args)
        dump_data(args)
        user_log.info("Pet name set")
        return "Pet Name Set"
    cmd_py_config["pet_name"]="PyOS v2.0"
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
        os.system(cmd_py_config["color"])
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
    auth.login.current_dir=auth.login.current_role=auth.login.current_user=None
    return " "

def apps(args):
    try:
        with open(sys_config_path) as sys_config:
            sys_py_config=json.loads(sys_config.read())
        apps_list=sys_py_config["apps"]
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

def color(args):
    colors_list={"blue":"color 1","green":"color 2","aqua":"color 3","red":"color 4","purple":"color 5",
                 "yellow":"color 6","white":"color 7","gray":"color 8","light blue":"color 9","light green":"color a",
                 "light aqua":"color b","light red":"color c","light purple":"color d","light yellow":"color e","default":"color f"}
    print("Choose your color theme:-")
    for count,color_name in enumerate(colors_list.keys()):
        print(f"{count+1}. {color_name.title()}",end="  ")
        if count+1 == 9:
            print()
    choice=input(f"\nPyOS:/home/{auth.login.current_user}/color_name> ").lower()
    if choice in colors_list:
        cmd_py_config["color"]=colors_list[choice]
        dump_data(None)
        os.system(colors_list[choice])
        return " "
    else:
        print("No color has been choosen!")
        return

def cmd(args):
    return "PyOS [version 2.0.00]\n(info) Python based kernel os.\n"

def os_info(args):
    if not args:
        return "Usage os --<info to be known>"
    
    with open(sys_config_path) as sys_config:
        sys_py_config=json.loads(sys_config.read())
    if args[0]=="--name":
        return "PyOS"
    elif args[0]=="--version":
        return sys_py_config["version"]
    elif args[0]=="--admin":
        return sys_py_config["admin"]
    return

def py_version(args):
    return cmd_py_config["python_version"]

def uptime(args):
    seconds=time.time()-boot_time
    return f"Up-time : {str(int(seconds//3600)).zfill(2)}:{str(int(seconds//60)).zfill(2)}:{str(int(seconds%60)).zfill(2)}"

def run(args):
    if not args:
        return "Usage: run <appname>"
    
    app_name=args[0]
    app_path=os.path.join(APPS_DIR,app_name+".py")

    if not (os.path.isfile(app_path)):
        return user_log.error(f"App: {app_name} not found")
    
    try:
        module=importlib.import_module(f"{APPS_DIR}.{app_name}")
        if not hasattr(module,"main"):
            return user_log.error("App has no main()")
        
        return module.main(auth.login.current_user,os.getcwd()+f"{auth.login.current_dir}\\{APPS_DIR}")
    except Exception as CMDError:
        return user_log.error("App crashed "+str(CMDError))

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
       #"ls":ls, lists all the files and dir in the cwd
       #"crdir":crdir, creates dir
       #"sd":sd, changes directory
       #"deldir":deldir, deletes dir
       #"copy":copy, copys and pastes the file or dir in another destination
       #"rename":rename, renames a file or dir
       #"delete":delete, deletes file
       #"cr":cr, creates an empty file in the current dir
       #"readf":readf, opens and displays the contents in a file
       #"man":man, manual for a particular cmd
       #"search":search, searchs a word in a file
       #"count":count , counts the number of words/letters/lines in a txt file
       "color":{"func":color,"permission":"user"},
       #"lock":lock, locks the os for a certain period of time
       "logout":{"permission":"user"},
       #reset os, resets the entire os only by admin
       #reset user, resets all the user profile without deleting user
       "pyver":{"func":py_version,"permission":"user"},
       "cmd":{"func":cmd,"permission":"user"},
       "os":{"func":os_info,"permission":"user"},
       "apps":{"func":apps,"permission":"users"},
       }

def execute(cmd):

    if auth.login.current_user is None:
       print("Not logged in")
       return
    
    try:
        part=cmd.split()
        if not part:
            return
        command=part[0]
        args=part[1:]
        if command in cmds:
            cmd_info=cmds[command]
            if cmd_info["permission"]=="admin": #and auth.login.current_role!="admin":
                user_log.critical("Permission Denied!")
                return
            output=cmd_info["func"](args)
            if output:
                print(output)
                user_log.info(f"cmd={cmd} Executed Successfully")
            else:
                user_log.error("Invalid Command "+cmd)
        else:
            user_log.error("Command Not Found")
    except Exception as CMDError:
            user_log.critical("Error CMD: "+str(CMDError))

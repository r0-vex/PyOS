import auth,fs
import os
import json
import random
from datetime import datetime
import calendar
import time

config_path=os.getcwd()+r"\system\config.json"

def load_data(args):
    try:
        with open(config_path) as cmd_config:
            cmd_py_config=json.loads(cmd_config.read())
    except FileNotFoundError:
        return fs.log.logger.critical("System Config Not Found")
    except Exception as CMDError:
        return fs.log.logger.error("ERROR 2: "+str(CMDError))
    return cmd_py_config

cmd_py_config=load_data(None)

def dump_data(args):
    try:
        with open(config_path,"w") as _sys_config:
            _sys_config.write(json.dumps(cmd_py_config))
    except FileNotFoundError:
        return fs.log.logger.critical("System Config Not Found")
    except Exception as CMDError:
        return fs.log.logger.error("ERROR 2: "+str(CMDError))
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
    return "Available Commands:-\n"+ "\n".join(cmds.keys())

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
        fs.log.logger.debug("Calendar Error: "+str(CalendarError))
        return
    year,month=int(datetime.now().strftime("%Y")),int(datetime.now().strftime("%m"))
    cal=calendar.TextCalendar(calendar.SUNDAY)
    month_calendar=cal.formatmonth(year,month)
    return month_calendar

def mood(args):
    moods=["shy\n(#^.^#)","excited\n(o_^)","productive\n\\(^-^)/","happy\n^-^","sad\n:-(","sleepy\n(-_-)zzz","bored\n:-o zz z z Z  Z"]
    return f"{cmd_py_config["pretty_name"]} is feeling "+random.choice(moods)

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
    systeminfo=["os_name","version","python_version","kernel","languages_used",
                "pretty_name","allowed_users","created_users","max_log"]
    sysinfo_keys=[key for key in cmd_py_config.keys() if key in systeminfo]
    return "\tSystem Information:-\n"+f"\n ".join(sysinfo_keys)

def setname(args):
    if args:
        cmd_py_config["pretty_name"]=" ".join(args)
        dump_data(args)
        fs.log.logger.info("Pretty name set")
        return "Pretty Name Set"
    cmd_py_config["pretty_name"]="PyOS v2.0"
    dump_data(args)
    return "Pretty Name Re-Setted"

def whoareu(args):
    return "I'm "+cmd_py_config["pretty_name"]

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

def add_user(args):
    return_val=auth.account_creation.user_create()
    return return_val

def logout(args):
    pass

cmds={"whoami": {"func":whoami,"permission":"user"},
       "clear": {"func":clear,"permission":"user"},
       "date": {"func":_date_,"permission":"user"},
       "time": {"func":_time_,"permission":"user"},
       "day": {"func":_day_,"permission":"user"},
       "greet": {"func":greet,"permission":"user"},
       "help":{"func":help,"permission":"user"},
       "echo":{"func":echo,"permission":"user"},
       "cal":{"func":_calendar_,"permission":"user"},
       "shutdown":None,
       "mood":{"func":mood,"permission":"user"},
       "quote":{"func":quote,"permission":"user"},
        "matrix":{"func":matrix,"permission":"user"},
       #"sysinfo":sysinfo,
       "setname":{"func":setname,"permission":"user"},
       "whoareu":{"func":whoareu,"permission":"user"},
       #"uptime":uptime, shows the total time spent
       #"run":run, runs apps
       "users":{"func":users,"permission":"admin"},
       "adduser":{"func":add_user,"permission":"admin"}
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
       #"color":color, change's os color for the current user
       #"lock":lock, locks the os for a certain period of time
       #"logout":logout, logs out the current user goes back to login screen
       }

def execute(cmd):
    try:
        part=cmd.split()
        if not part:
            return
        command=part[0]
        args=part[1:]
        if command in cmds:
            cmd_info=cmds[command]
            if cmd_info["permission"]=="admin": #and auth.login.current_role!="admin":
                fs.log.logger.critical("Permission Denied!")
                return
            output=cmd_info["func"](args)
            if output:
                print(output)
                fs.log.logger.info(cmd+" Executed Successfully")
            else:
                fs.log.logger.error("Invalid Command "+cmd)
        else:
            fs.log.logger.error("Command Not Found")
    except Exception as CMDError:
            fs.log.logger.critical("Error CMD: "+str(CMDError))

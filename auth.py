import os
import json
import time
import fs,security
from logger import Logger
import getpass

class TooShort(Exception):
     pass
class TooLong(Exception):
     pass
class SpecialChar(Exception):
     pass
class ReservedWord(Exception):
     pass

class MissingDigit(Exception):
     pass
class MissingLowerCase(Exception):
     pass
class MissingUpperCase(Exception):
     pass
class SpaceError(Exception):
    pass

class UserNotFound(Exception):
     pass
class IncorrectPassword(Exception):
     pass

sys_log=Logger.system()
global auth_py_config
#loading auth config
try:
    config_path=os.getcwd()+r"\system\config.json"
    with open(config_path) as auth_sys_config: 
        auth_py_config=json.loads(auth_sys_config.read())

    users=auth_py_config["users"]
    sys_log.info("System Config Loaded Successfully in auth.py")

except FileNotFoundError:
        sys_log.error("ERROR 1: Unable to load auth")
except Exception as AuthError:
    sys_log.critical("Auth load failed: " + str(AuthError))
    raise SystemExit

#reloading auth config
def load_data():
    global auth_py_config
    try:
        with open(config_path) as auth_sys_config: 
            auth_py_config=json.loads(auth_sys_config.read())
        global users
        users=auth_py_config["users"]
        sys_log.info("System Config Re-Loaded Successfully in auth.py")

    except FileNotFoundError:
        sys_log.error("ERROR 1: Unable to load auth")
    except Exception as AuthError:
        sys_log.critical("Auth load failed: " + str(AuthError))
        raise SystemExit

#rewriting auth config
def dump_data():
        global auth_py_config
        try:
            with open(config_path,"w") as auth_sys_config:
                json.dump(auth_py_config,auth_sys_config,indent=4)
            sys_log.info("System Config Overwritten Successfully.")
        except FileNotFoundError:
                sys_log.error("ERROR 1: Unable to re-load config in auth.py")
        except Exception as AuthError:
                sys_log.error("ERROR 1a Config save failed: "+str(AuthError))
        else:
             load_data()
        
def validate_username(mode="user"):
    while True:
        invalid_char=set()
        try:
            user_name=input(f"PyOS:/create/{mode}_name> ").replace(" ","_")
            if mode=="user":
                 if user_name in users or user_name==auth_py_config["admin"]:
                    sys_log.warning("User already exists")
                    continue
            if user_name=="":
                sys_log.warning("Username Invalid!")
                continue
            elif user_name.lower() in ["root","admin","system","user","users","null"]:
                 raise ReservedWord
            elif 8>len(user_name):
                raise TooShort
            elif 16<len(user_name):
                raise TooLong
            for j in user_name:
                if j in """=&'-$!"`\\;|/,<>^+""" or ord(j)>126 or ord(j)<32:
                    invalid_char.add(j)
            if not invalid_char:
                return user_name
            raise SpecialChar
        except TooShort:
            sys_log.warning("User Name too Short")
        except TooLong:
            sys_log.warning("User Name too Long")
        except SpecialChar:
            sys_log.warning("Invalid Characters: "+"".join(invalid_char))
        except ReservedWord:
            sys_log.warning("Reserved names can't be username")
        except KeyboardInterrupt:
            sys_log.warning("Exiting...")
            return False
        except Exception as UserValidation:
            sys_log.error("ERROR 1: "+str(UserValidation))

def validate_password(mode="user"):
    while True:
        invalid_char=set()
        digit_count=letter_upper=letter_lower=sp_char=0
        print("Enter PyOS Password:")
        try:
            try:
                user_password=getpass.getpass(prompt=f"PyOS:/create/{mode}_password> ")
            except getpass.GetPassWarning:
                sys_log.warning("Warning: Secure password input unavailable")
                user_password = input(f"PyOS:/create/{mode}_password> ")
            if user_password=="":
                sys_log.warning("Invalid Password: Password can't be empty")
                continue
            elif 8>len(user_password):
                raise TooShort
            elif 16<len(user_password):
                raise TooLong
            elif " " in user_password:
                raise SpaceError
            for j in user_password:
                if ord(j)>126 or ord(j)<32:
                    invalid_char.add(j)
                    continue
                if j.isdigit():
                    digit_count+=1
                elif j.isupper():
                    letter_upper+=1
                elif j.islower():
                    letter_lower+=1
                elif j in "@*#._%":
                    sp_char+=1
                else:
                    invalid_char.add(j)
            if invalid_char:
                print("Invalid Characters: ",invalid_char)
                continue
            if digit_count<2:
                raise MissingDigit
            elif letter_lower<2:
                raise MissingLowerCase
            elif letter_upper<2:
                raise MissingUpperCase
            elif sp_char<1:
                raise SpecialChar
            print("Re-Enter your password")
            try:
                confirm=getpass.getpass(prompt=f"PyOS:/create/{mode}_password> ")
            except getpass.GetPassWarning:
                sys_log.warning("Warning: Secure password input unavailable")
                confirm= input(f"PyOS:/create/{mode}_password> ")
            if user_password!=confirm:
                print("Passwords don't match")
                continue
            return user_password
        except TooShort:
            sys_log.warning("Password Too Short")
        except TooLong:
            sys_log.warning("Password Too Long")
        except MissingDigit:
            sys_log.warning("Should have atleast 2 digits")
        except MissingLowerCase:
            sys_log.warning("Should have atleast 2 Lowercase")
        except MissingUpperCase:
            sys_log.warning("Should have atleast 2 Uppercase")
        except SpecialChar:
            sys_log.warning("Should have atleast any one of @ * # . _ %")
        except SpaceError:
            sys_log.warning("Should not contain Space")
        except KeyboardInterrupt:
            sys_log.warning("Exiting...")
            return False 
        except Exception as PasswordValidation:
            sys_log.error("ERROR 1:"+str(PasswordValidation))
     
class account_creation():
    def admin_create():
        try:
            print("\nCreate your PyOS Name")
            print("Spaces are not allowed,if exists WILL BE REPLACED WITH _")
            admin_name=validate_username("admin")
            if not admin_name:
                return False
            admin_password=validate_password("admin")
            if not admin_password:
                return False
            hash,salt=security.PasswordManager.hash_password(admin_password)
            auth_py_config["admin"]=admin_name
            auth_py_config["admin_password"]={"hash":hash,"salt":salt,}
            fs.user_files_creation.create_user_files(admin_name,security.SYSTEM_ROLE,True)
            auth_py_config["boot_flag"]=False
            dump_data()
            sys_log.info("OS Admin created successfully.")
            print("OS Admin created successfully. ",end="")
            for _ in range(3):
                time.sleep(0.5)
                print(". ",end="",flush=True)
            print()
            return True
        except Exception as CreationError:
            sys_log.error("ERROR 1b: "+str(CreationError))
    def user_create():
        try:
            if auth_py_config["allowed_users"]>auth_py_config["created_users"]:
                print("\nCreate your PyOS Name")
                print("Spaces are not allowed,if exists WILL BE REPLACED WITH _")
                u_name=validate_username()
                if not u_name:
                    return False
                u_password=validate_password()
                if not u_password:
                    return False
                hash,salt=security.PasswordManager.hash_password(u_password)
                auth_py_config["users"].append(u_name)
                auth_py_config["users_hash"].append({"hash":hash,"salt":salt})
                auth_py_config["created_users"]+=1
                fs.user_files_creation.create_user_files(u_name,security.SYSTEM_ROLE)
                dump_data()
                sys_log.info(f"{u_name} :User created successfully.")
                print("User created successfully. ",end="")
                for _ in range(3):
                    time.sleep(0.5)
                    print(". ",end="",flush=True)
                print()
                return True
            else:
                sys_log.error("No. of users limit: 5 Exceeded")
                return False
        except Exception as CreationError:
            sys_log.error("ERROR 1b: "+str(CreationError))
            return False

class login():
    current_user=None
    current_role=None
    current_dir=None
    user_dir=None

    def users_list():
        try:
            print(f'1. {auth_py_config["admin"]} (Admin)')
            for user_number,user in enumerate(users):
                print(f"{user_number+2}. {user}")
        except Exception as MenuError:
             sys_log.error("ERROR 1g: "+str(MenuError))
    def auth_login():
        login_attempt=5
        try:
            while login_attempt>0:
                user=input("\nPyOS:/login/user_name> ")
                if user==auth_py_config["admin"]:
                    login.current_user = user
                    password=auth_py_config["admin_password"]["hash"]
                    key=auth_py_config["admin_password"]["salt"]
                    try:
                        a_password=getpass.getpass(prompt="PyOS:/login/password> ")
                    except getpass.GetPassWarning:
                        sys_log.warning("Warning: Secure password input unavailable")
                        a_password = input("PyOS:/login/password> ")
                    if security.PasswordManager.verify_password(a_password,password,key):
                            login.current_user=user
                            login.current_role="admin"
                            login.current_dir=os.path.join("users",user,"home")
                            login.user_dir=os.path.join("users",user)
                            return True
                    login_attempt-=1
                    sys_log.error("ERROR 1j: Incorrect Password")
                    continue
                elif user in users:
                    login.current_user = user
                    user_index=users.index(user)
                    password_dict=auth_py_config["users_hash"][user_index]
                    key=password_dict["salt"]
                    password=password_dict["hash"]
                    u_password=getpass.getpass(prompt="PyOS:/login/password> ",stream=None)
                    if security.PasswordManager.verify_password(u_password,password,key):
                        login.current_user=user
                        login.current_role="user"
                        login.current_dir=os.path.join("users",user,"home")
                        login.user_dir=os.path.join("users",user)
                        return True
                    login_attempt-=1
                    sys_log.error("ERROR 1j: Incorrect Password")
                    continue
                login_attempt-=1
                sys_log.error("ERROR 1h: User Not Found")
            return False
        except KeyboardInterrupt:
            sys_log.error("ERROR 1k: Forced Shutdown")
            return False
        except Exception as LoginError:
                sys_log.error("ERROR 1i: "+str(LoginError))
    
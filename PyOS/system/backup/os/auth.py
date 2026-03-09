import os
import json
import time
import fs,security


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

#loading auth config
try:
    config_path=os.getcwd()+r"\system\config.json"
    with open(config_path) as auth_sys_config: 
        auth_py_config=json.loads(auth_sys_config.read())

    users=auth_py_config["users"]
    fs.log.logger.info("System Config Loaded Successfully in auth.py")

except FileNotFoundError:
        fs.log.logger.error("ERROR 1: Unable to load auth")
except Exception as AuthError:
    fs.log.logger.critical("Auth load failed: " + str(AuthError))
    raise SystemExit
#reloading auth config
def load_data():
    try:
        with open(config_path) as auth_sys_config: 
            auth_py_config=json.loads(auth_sys_config.read())

        users=auth_py_config["users"]
        fs.log.logger.info("System Config Re-Loaded Successfully in auth.py")

    except FileNotFoundError:
        fs.log.logger.error("ERROR 1: Unable to load auth")
    except Exception as AuthError:
        fs.log.logger.critical("Auth load failed: " + str(AuthError))
        raise SystemExit
#rewriting auth config
def dump_data():
        try:
            with open(config_path,"w") as auth_sys_config: 
                 auth_sys_config.write(json.dumps(auth_py_config))

            fs.log.logger.info("System Config Overwritten Successfully.")
        except FileNotFoundError:
                fs.log.logger.error("ERROR 1: Unable to load re-load config in auth.py")
        except Exception as AuthError:
                fs.log.logger.error("ERROR 1a Config save failed: "+str(AuthError))
        else:
             load_data()
        
def validate_username(mode="user"):
    while True:
        invalid_char=set()
        try:
            user_name=input(f"PyOS:/create/{mode}_name> ").replace(" ","_")
            if mode=="user":
                 if user_name in users or user_name==auth_py_config["admin"]:
                    fs.log.logger.warning("User already exists")
                    continue
            if user_name=="":
                fs.log.logger.warning("Username Invalid!")
                continue
            elif 8>len(user_name):
                raise TooShort
            elif 16<len(user_name):
                raise TooLong
            elif user_name.lower() in ["root","admin","system","user","users","null"]:
                 raise ReservedWord
            for j in user_name:
                if j in """=&'-$!"`\\;|/,<>^+""" or ord(j)>126 or ord(j)<32:
                    invalid_char.add(j)
            if not invalid_char:
                return user_name
            raise SpecialChar
        except TooShort:
            fs.log.logger.warning("User Name too Short")
        except TooLong:
            fs.log.logger.warning("User Name too Long")
        except SpecialChar:
            fs.log.logger.warning("Invalid Characters: "+invalid_char)
        except ReservedWord:
            fs.log.logger.warning("Reserved names can't be username")
        except Exception as UserValidation:
            fs.log.logger.error("ERROR 1: "+str(UserValidation))

def validate_password(mode="user"):
    while True:
        invalid_char=set()
        digit_count=letter_upper=letter_lower=sp_char=0
        print("Enter PyOS Password")
        try:
            user_password=input(f"PyOS:/create/{mode}_password> ")
            if user_password=="":
                fs.log.logger.warning("Invalid Password: Password can't be empty")
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
            confirm=input(f"PyOS:/{mode}_password> ")
            if user_password!=confirm:
                print("Passwords don't match")
                continue
            return user_password
        except TooShort:
            fs.log.logger.warning("Password Too Short")
        except TooLong:
            fs.log.logger.warning("Password Too Long")
        except MissingDigit:
            fs.log.logger.warning("Should have atleast 2 digits")
        except MissingLowerCase:
            fs.log.logger.warning("Should have atleast 2 Lowercase")
        except MissingUpperCase:
            fs.log.logger.warning("Should have atleast 2 Uppercase")
        except SpecialChar:
            fs.log.logger.warning("Should have atleast any one of @ * # . _ %")
        except SpaceError:
            fs.log.logger.warning("Should not contain Space")
        except Exception as PasswordValidation:
            fs.log.logger.error("ERROR 1:"+str(PasswordValidation))
     

class account_creation():
    def admin_create():
        try:
            print("\nCreate your PyOS Name")
            print("Spaces are not allowed,if exists WILL BE REPLACED WITH _")
            admin_name=validate_username("admin")
            admin_password=validate_password("admin")
            hash,salt=security.hash_password(admin_password)
            auth_py_config["admin"]=admin_name
            auth_py_config["admin_password"]={"hash":hash,"salt":salt,}
            fs.file.create_dir(r"\users\admin")
            auth_py_config["boot_flag"]=False
            dump_data()
            fs.log.logger.info("OS Admin created successfully.")
            print("OS Admin created successfully. ",end="")
            for _ in range(3):
                time.sleep(0.5)
                print(". ",end="",flush=True)
            print()
            return
        except Exception as CreationError:
            fs.log.logger.error("ERROR 1b: "+str(CreationError))
    def user_create():
        try:
            if auth_py_config["allowed_users"]>=auth_py_config["created_users"]:
                print("\nCreate your PyOS Name")
                print("Spaces are not allowed,if exists WILL BE REPLACED WITH _")
                u_name=validate_username()
                u_password=validate_password()
                hash,salt=security.hash_password(u_password)
                auth_py_config["users"].append(u_name)
                auth_py_config["users_hash"].append({"hash":hash,"salt":salt})
                auth_py_config["created_users"]+=1
                fs.file.create_dir("\\users\\"+u_name)
                dump_data()
                fs.log.logger.info("User created successfully.")
                print("User created successfully. ",end="")
                for _ in range(3):
                    time.sleep(0.5)
                    print(". ",end="",flush=True)
                print()
                return " "
            else:
                fs.log.logger.error("No. of users limit: 5 Exceeded")
                return
        except Exception as CreationError:
            fs.log.logger.error("ERROR 1b: "+str(CreationError))

class login():
    current_user= None
    current_role=None
    current_dir=None
    def users_list():
        try:
            print(f'1. {auth_py_config["admin"]} (Admin)')
            for user_number,user in enumerate(users):
                print(f"{user_number+2}. {user}")
        except Exception as MenuError:
             fs.log.logger.error("ERROR 1g: "+str(MenuError))
    def auth_login():
        login_attempt=5
        try:
            while login_attempt>0:
                user=input("\nPyOS:/login/user_name> ")
                if user==auth_py_config["admin"]:
                    password=auth_py_config["admin_password"]["hash"]
                    key=auth_py_config["admin_password"]["salt"]
                    a_password=input("PyOS:/login/password> ")
                    if security.verify_password(a_password,password,key):
                            login.current_user=user
                            login.current_role="admin"
                            login.current_dir=r"\users\admin"
                            fs.log.logger.info("Login Successful...")
                            return True
                    login_attempt-=1
                    fs.log.logger.error("ERROR 1j: Incorrect Password")
                    continue
                elif user in users:
                    user_index=users.index(user)
                    password_dict=auth_py_config["users_hash"][user_index]
                    key=password_dict["salt"]
                    password=password_dict["hash"]
                    u_password=input("PyOS:/login/password> ")
                    if security.verify_password(u_password,password,key):
                        login.current_user=user
                        login.current_role="user"
                        login.current_dir=r"\users"+user
                        fs.log.logger.info("Login Successful...")
                        return True
                    login_attempt-=1
                    fs.log.logger.error("ERROR 1j: Incorrect Password")
                    continue
                login_attempt-=1
                fs.log.logger.error("ERROR 1h: User Not Found")
            return False
        except Exception as LoginError:
                fs.log.logger.error("ERROR 1i: "+str(LoginError))
    
    def require_admin():
        return login.current_role=="admin"
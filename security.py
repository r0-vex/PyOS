import secrets
import os
from hashlib import sha256
from logger import Logger

class NoAccessError(Exception):
    pass

PyOS_path=os.getcwd()
sys_log=Logger.system()

SYSTEM_ROLE="PyOS"
SYSTEM_PROTECTED = [os.path.abspath(os.path.join(PyOS_path, "system")),]
SYSTEM_FILES = ["main.py","fs.py","auth.py","security.py","commands.py","logger.py","boot.bat"]
USER_PROTECTED = ["config.json","log.txt"]
RESERVED_USER_DIRS = ["system","apps","home"]

class PasswordManager:

    @staticmethod
    def hash_password(password):
        salt=secrets.token_hex(8)
        combined=password+salt
        hash_value=sha256(combined.encode()).hexdigest()
        return hash_value,salt

    @staticmethod
    def verify_password(password,hash_value,salt):
        combined=password+salt
        return sha256(combined.encode()).hexdigest()==hash_value

class AccessControl:

    @staticmethod
    def safe_path(path):
            try:
                final_path = os.path.abspath(os.path.join(PyOS_path, path))
                # Prevent escaping
                if os.path.commonpath([final_path, PyOS_path]) != PyOS_path:
                    raise PermissionError
                return final_path
            except PermissionError:
                sys_log.error("Path Escape Detected!")
                print("Permission Denied!")
                return None

            except Exception as PathError:
                sys_log.error("PATH ERROR: " + str(PathError))
                return None
            
    @staticmethod
    def check_permission(safe_path, current_role, current_user, operation="read"):
        try:
            if safe_path is None:
                return False
            if current_role == SYSTEM_ROLE:
                return True
            allowed_root = os.path.abspath(os.path.join(PyOS_path, "users", current_user))
            if os.path.commonpath([safe_path, allowed_root]) != allowed_root:
                raise NoAccessError
            relative = os.path.relpath(safe_path,allowed_root)
            parts = relative.split(os.sep)
            if parts and parts[0] in ["system", "apps"]:
                if current_role != SYSTEM_ROLE:
                        raise NoAccessError
            if len(parts) == 1 and parts[0] in RESERVED_USER_DIRS:
                if operation in ["delete", "write"]:
                    raise NoAccessError
            for protected in SYSTEM_PROTECTED:
                if os.path.commonpath([safe_path, protected]) == protected:
                    raise NoAccessError
            if os.path.basename(safe_path) in SYSTEM_FILES:
                raise NoAccessError
            return True
        except NoAccessError:
            sys_log.error(f"Invalid Destination Path")
            print("Access Denied!")
            return False
        except Exception as PermissionError:
            sys_log.error("PERMISSION ERROR: " + str(PermissionError))
            return False
    
    @staticmethod
    def authorize(path, role, user, operation="read"):
        safe = AccessControl.safe_path(path)
        if safe is None:
            return None
        if not AccessControl.check_permission(safe,role,user,operation):
            return None
        return safe
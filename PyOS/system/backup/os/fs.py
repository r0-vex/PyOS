import logging
import os

class log:
    logger=logging.getLogger("PyOS") #setting name to logger
    logger.setLevel(logging.DEBUG)

    console_handler=logging.StreamHandler() #setting consoler
    console_handler.setLevel(logging.WARNING)

    file_handler=logging.FileHandler(os.getcwd()+r"\system\log.txt","a+") #setting file handler
    file_handler.setLevel(logging.DEBUG)

    formatter=logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s") #log format

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)  # setting format to handlers

    logger.addHandler(file_handler)
    logger.addHandler(console_handler) #setting handlers to logger

class file(log):
    def create_dir(path):
        try:
            if not (os.path.exists(os.getcwd()+path)):
                os.mkdir(os.getcwd()+path)
                log.logger.info(os.getcwd()+path+" Directory Created")
        except FileExistsError:
            log.logger.error("ERROR 2a: Directory Exists")
        except Exception as FileCreationError:
            log.logger.error("ERROR 2b: "+str(FileCreationError))

#the os checks for lock if locked asks for admin password to unlock it
#then login page opens
#intially the user logs in
#if user types logsout
#then login page reappears with resetting the auth.login.var_name

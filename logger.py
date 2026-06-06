import logging
import os

class Logger:
    @staticmethod
    def get_logger(name,path,console_level=logging.WARNING,file_level=logging.DEBUG):

        logger = logging.getLogger(name)

        if logger.handlers:
            return logger
        
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(name)s: %(message)s")

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(formatter)

        # File Handler
        file_handler = logging.FileHandler(os.path.join(os.getcwd(), path),"a+",encoding="utf-8")
        file_handler.setLevel(file_level)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    @staticmethod
    def system():
        return Logger.get_logger("System Log",os.path.join("system", "log.txt"))

    @staticmethod
    def user(username):
        return Logger.get_logger(f"{username} Log",os.path.join("users",username,"system","log.txt"))

    @staticmethod
    def backup():
        return Logger.get_logger("Backup Log",os.path.join("system","backup","logs","backup.log"))
    
    @staticmethod
    def trim_log(path,max_log,log):
        try:
            if not os.path.exists(path):
                log.info("No Log Found")
                return False
            with open(path) as log_file:
                log_before_trim=log_file.readlines()
                len_log_before_trim=len(log_before_trim)
                if len_log_before_trim <= max_log:
                    return False
            log_after_trim=log_before_trim[-max_log:]
            len_log_after_trim=len(log_after_trim)
            with open(path,"w") as log_file:
                log_file.writelines(log_after_trim)
            log.info(f"Auto Trim: {len_log_before_trim} to {len_log_after_trim} entries")
            return True
        except FileNotFoundError:
            log.error("Log Not Found")
            return False
        except Exception as LogError:
            log.error("ERROR TRIM: "+str(LogError))
            return False
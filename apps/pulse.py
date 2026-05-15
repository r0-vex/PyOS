import os
import random
import json
import commands
import auth
import fs


class Pulse:
    def __init__(self, username):
        self.username = username
        self.name = "Pulse"
        self.version = "v3.0"
        # memory
        self.current_topic = None
        self.last_command = None
        self.last_problem = None
        self.last_app = None
        # load dynamic system data
        self.commands = commands.cmds
        self.apps = self.load_apps()
        # intents
        self.greetings = {
            "hi", "hello", "hey", "yo", "yoo"
        }
        self.byes = {
            "bye", "exit", "cya", "goodbye"
        }
        # dangerous commands
        self.dangerous_cmds = {
            "delete",
            "deluser",
            "shutdown",
            "reset"
        }
        # troubleshooting db
        self.troubleshoot = {
            "wifi": {
                "causes": [
                    "DNS issue",
                    "adapter disabled",
                    "router unreachable"
                ],
                "fixes": [
                    "Reconnect network",
                    "Restart router",
                    "Refresh adapter"
                ],
                "commands": [
                    "ping",
                    "netstat",
                    "ifconfig"
                ]
            },

            "disk": {
                "causes": [
                    "Low storage",
                    "filesystem corruption",
                    "junk files"
                ],

                "fixes": [
                    "Delete unnecessary files",
                    "Clean temporary data",
                    "Check storage usage"
                ],

                "commands": [
                    "ls",
                    "delete",
                    "count"
                ]
            },

            "performance": {
                "causes": [
                    "High CPU usage",
                    "Low RAM",
                    "Too many apps"
                ],

                "fixes": [
                    "Close apps",
                    "Restart PyOS",
                    "Reduce background tasks"
                ],

                "commands": [
                    "sysinfo",
                    "matrix"
                ]
            }
        }
    # ------------------------------
    # load apps
    # ------------------------------
    def load_apps(self):

        try:
            return os.listdir(os.path.join(os.getcwd(),"apps"))

        except Exception:
            return []

    # ------------------------------
    # tokenize
    # ------------------------------

    def tokenize(self, text):
        return text.lower().strip().split()

    # ------------------------------
    # greeting
    # ------------------------------

    def handle_greeting(self):

        replies = [

            f"Hey {self.username} 😄",

            f"Welcome back {self.username}.",

            "Pulse online.",

            "Ready to assist."
        ]

        return random.choice(replies)
    # ------------------------------
    # farewell
    # ------------------------------

    def handle_bye(self):
        replies = [

            "Pulse signing off.",

            "See ya 😄",

            "Logging out of conversation."
        ]
        return random.choice(replies)

    # -----------------------------
    # show commands
    # ------------------------------

    def available_commands(self):

        cmd_list = list(self.commands.keys())

        return (
            "Available Commands:\n\n" +
            "\n".join(cmd_list)
        )

    # ------------------------------
    # explain command
    # ------------------------------

    def explain_command(self, words):

        for cmd in self.commands:

            if cmd in words:

                self.last_command = cmd

                cmd_info = self.commands[cmd]

                permission = cmd_info["permission"]

                return (
                    f"Command: {cmd}\n"
                    f"Permission: {permission}"
                )

        return None

    # ------------------------------
    # execute commands
    # ------------------------------

    def execute_command(self, cmd):

        try:

            self.last_command = cmd

            if cmd in self.dangerous_cmds:

                confirm = input(
                    f"Pulse> Dangerous command '{cmd}'. Continue? (y/n): "
                )

                if confirm.lower() != "y":
                    return "Command aborted."

            commands.execute(cmd)

            return f"Executed: {cmd}"

        except Exception as CommandError:

            return f"Execution Error: {CommandError}"

    # ------------------------------
    # open apps
    # ------------------------------

    def open_app(self, words):

        for app in self.apps:

            app_name = app.replace(".py", "")

            if app_name in words:

                self.last_app = app_name

                commands.execute(f"run {app_name}")

                return f"Launching {app_name}..."

        return None

    # ------------------------------
    # troubleshoot
    # ------------------------------

    def diagnose(self, issue):

        self.current_topic = issue
        self.last_problem = issue

        data = self.troubleshoot[issue]

        causes = "\n".join(
            [f"- {x}" for x in data["causes"]]
        )

        fixes = "\n".join(
            [f"- {x}" for x in data["fixes"]]
        )

        cmds = "\n".join(
            [f"- {x}" for x in data["commands"]]
        )

        return (
            f"Problem Detected: {issue}\n\n"
            f"Possible Causes:\n{causes}\n\n"
            f"Possible Fixes:\n{fixes}\n\n"
            f"Recommended Commands:\n{cmds}"
        )

    # ------------------------------
    # auto fix
    # ------------------------------

    def auto_fix(self, issue):

        if issue == "wifi":

            return (
                "Attempting network recovery...\n"
                "Refreshing adapter...\n"
                "DNS cache cleared."
            )

        elif issue == "disk":

            return (
                "Analyzing storage...\n"
                "Junk file scan completed."
            )

        elif issue == "performance":

            return (
                "Checking background apps...\n"
                "Memory optimization recommended."
            )

        return "Unable to auto-fix problem."

    # ------------------------------
    # analyze logs
    # ------------------------------

    def analyze_logs(self):

        try:

            log_path = os.path.join(os.getcwd(),"system","log.txt")

            with open(log_path, "r") as file:

                logs = file.readlines()

            recent = logs[-5:]

            return (
                "Recent System Logs:\n\n" +
                "".join(recent)
            )

        except Exception:

            return "Unable to analyze logs."

    # ------------------------------
    # contextual memory
    # ------------------------------

    def contextual_reply(self, text):

        if text == "how":

            if self.current_topic == "wifi":

                return (
                    "Try:\n"
                    "1. reconnect wifi\n"
                    "2. restart router\n"
                    "3. refresh adapter"
                )

            elif self.current_topic == "disk":

                return (
                    "Use:\n"
                    "ls -> list files\n"
                    "delete -> remove junk"
                )

        return None

    # ------------------------------
    # suggestions
    # ------------------------------

    def suggest_command(self, text):

        suggestions = {

            "create file": "Use: cr notes.txt",

            "remove file": "Use: delete notes.txt",

            "make folder": "Use: mkdir projects",

            "list files": "Use: ls",

            "run app": "Use: run <appname>"
        }

        for key in suggestions:

            if key in text:
                return suggestions[key]

        return None

    # ------------------------------
    # intent engine
    # ------------------------------

    def respond(self, text):

        text = text.lower().strip()

        words = self.tokenize(text)

        # greetings
        if any(word in self.greetings for word in words):

            return self.handle_greeting()

        # bye
        if any(word in self.byes for word in words):

            return self.handle_bye()

        # thanks
        if "thanks" in words:

            return f"Always happy to help, {self.username} 😄"

        # show commands
        if "commands" in words:

            return self.available_commands()

        # explain commands
        if "help" in words or "use" in words:

            command_response = self.explain_command(words)

            if command_response:
                return command_response

        # app launching
        if "open" in words or "run" in words:

            app_response = self.open_app(words)

            if app_response:
                return app_response

        # troubleshooting
        for issue in self.troubleshoot:

            if issue in words:

                return self.diagnose(issue)

        # auto fixing
        if "fix" in words:

            if self.last_problem:

                return self.auto_fix(self.last_problem)

        # execute shell commands naturally
        if text == "show files":

            return self.execute_command("ls")

        elif text == "who am i":

            return self.execute_command("whoami")

        elif text == "start matrix":

            return self.execute_command("matrix")

        elif text == "show quote":

            return self.execute_command("quote")

        # logs
        if "logs" in words:

            return self.analyze_logs()

        # contextual replies
        context = self.contextual_reply(text)

        if context:
            return context

        # suggestions
        suggestion = self.suggest_command(text)

        if suggestion:
            return suggestion

        # installed apps
        if "apps" in words:

            return (
                "Installed Apps:\n\n" +
                "\n".join(self.apps)
            )

        # system info
        if "version" in words:

            return (
                f"PyOS Version 2.0\n"
                f"Pulse Version: {self.version}"
            )

        # fallback
        return (
            "Hmm... I didn't understand that.\n"
            "Try asking about:\n"
            "- commands\n"
            "- apps\n"
            "- wifi\n"
            "- disk\n"
            "- performance\n"
            "- logs"
        )


# ------------------------------
# main loop
# ------------------------------

def main(username, args=None):

    pulse = Pulse(username)

    print(f"{pulse.name} {pulse.version} Online...")
    print("AI Shell Ready.\n")

    while True:

        try:

            user_input = input(f"{username}> ")

            if not user_input.strip():
                continue

            response = pulse.respond(user_input)

            print(f"Pulse> {response}\n")

            if "bye" in user_input.lower():
                return "Exited"

        except KeyboardInterrupt:

            print("\nPulse Interrupted.")
            break

        except Exception as PulseError:

            print(f"Pulse Error: {PulseError}")


if __name__ == "__main__":

    main(auth.login.current_user)
import random
import commands
import auth
import os


class Pulse:

    def __init__(self, username):

        self.name = "Pulse"
        self.version = "v2.0"
        self.username = username

        # memory
        self.current_topic = None
        self.last_command = None
        self.last_app = None
        self.last_problem = None

        # intents
        self.greetings = {"hi", "hello", "hey", "yo", "yoo"}
        self.byes = {"bye", "cya", "goodbye", "exit"}

        # troubleshooting database
        self.troubleshoot = {

            "wifi": {
                "causes": [
                    "DNS failure",
                    "adapter disabled",
                    "IP conflict"
                ],

                "solutions": [
                    "Reconnect wifi",
                    "Restart router",
                    "Check DNS settings"
                ],

                "commands": [
                    "ping",
                    "ifconfig",
                    "netstat"
                ]
            },

            "disk": {
                "causes": [
                    "Storage full",
                    "Filesystem corruption",
                    "Too many junk files"
                ],

                "solutions": [
                    "Delete unnecessary files",
                    "Check filesystem",
                    "Clean storage"
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
                    "Low memory",
                    "Too many background apps"
                ],

                "solutions": [
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

        # command explanations
        self.command_help = {

            "help": "Shows all commands.\nUsage: help",

            "count": (
                "Counts words, letters and lines.\n"
                "Examples:\n"
                "count -w notes.txt\n"
                "count -line notes.txt"
            ),

            "ls": "Lists files and folders.\nUsage: ls",

            "delete": "Deletes a file.\nUsage: delete file.txt",

            "mkdir": "Creates a folder.\nUsage: mkdir projects",

            "run": "Runs PyOS apps.\nUsage: run notes",

            "whoami": "Displays current user.",

            "matrix": "Starts matrix mode 😈",

            "quote": "Displays random quote.",

            "shutdown": "Shuts down PyOS safely."
        }

        # app aliases
        self.apps = {
            "vault": "run vault",
            "notes": "run notes",
            "guess": "run guess",
            "pulse": "run pulse"
        }

    # tokenize input
    def tokenize(self, text):
        return text.lower().strip().split()

    # check word
    def contains(self, words, targets):
        return any(word in targets for word in words)

    # greeting handler
    def handle_greeting(self):

        replies = [
            f"Hey {self.username} 😄",
            f"Yo {self.username}.",
            f"Welcome back {self.username}.",
            "Pulse online.",
            "Ready to assist."
        ]

        return random.choice(replies)

    # bye handler
    def handle_bye(self):

        replies = [
            "See ya 😄",
            "Pulse signing off.",
            "Logging out of conversation.",
            "Catch you later."
        ]

        return random.choice(replies)

    # command list
    def available_commands(self):

        try:

            cmd_list = list(commands.cmds.keys())

            return (
                "Available Commands:\n\n" +
                "\n".join(cmd_list)
            )

        except Exception:
            return "Unable to load commands."

    # explain command
    def explain_command(self, words):

        for cmd in self.command_help:

            if cmd in words:
                self.last_command = cmd
                return self.command_help[cmd]

        return None

    # troubleshooting engine
    def diagnose(self, issue):

        self.current_topic = issue
        self.last_problem = issue

        data = self.troubleshoot[issue]

        causes = "\n".join(
            [f"- {x}" for x in data["causes"]]
        )

        solutions = "\n".join(
            [f"- {x}" for x in data["solutions"]]
        )

        cmds = "\n".join(
            [f"- {x}" for x in data["commands"]]
        )

        return (
            f"Possible Causes:\n{causes}\n\n"
            f"Solutions:\n{solutions}\n\n"
            f"Useful Commands:\n{cmds}"
        )

    # launch apps
    def open_app(self, words):

        for app in self.apps:

            if app in words:

                self.last_app = app

                try:
                    commands.execute(self.apps[app])
                    return f"Launching {app}..."

                except Exception as AppError:
                    return f"App Launch Error: {AppError}"

        return None

    # execute commands directly
    def execute_shell(self, words):

        command_alias = {

            "show files": "ls",
            "list files": "ls",
            "who am i": "whoami",
            "start matrix": "matrix",
            "show quote": "quote",
            "shutdown pyos": "shutdown"
        }

        joined = " ".join(words)

        for sentence in command_alias:

            if sentence == joined:

                cmd = command_alias[sentence]

                try:
                    self.last_command = cmd
                    commands.execute(cmd)

                    return f"Executed: {cmd}"

                except Exception as CommandError:
                    return f"Execution Error: {CommandError}"

        return None

    # suggest commands
    def suggest_command(self, text):

        text = text.lower()

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

    # contextual replies
    def contextual_reply(self, text):

        if text == "how":

            if self.current_topic == "wifi":

                return (
                    "Try:\n"
                    "1. reconnect wifi\n"
                    "2. restart router\n"
                    "3. check DNS"
                )

            elif self.current_topic == "disk":

                return (
                    "Use:\n"
                    "ls -> list files\n"
                    "delete -> remove junk files"
                )

        return None

    # system info
    def system_info(self, text):

        if "version" in text:
            return f"PyOS Version 2.0 | Pulse {self.version}"

        elif "user" in text:
            return f"Current User: {auth.login.current_user}"

        elif "apps" in text:
            return (
                "Installed Apps:\n" +
                "\n".join(self.apps.keys())
            )

        return None

    # main response engine
    def respond(self, text):

        text = text.lower().strip()
        words = self.tokenize(text)

        # greeting
        if self.contains(words, self.greetings):
            return self.handle_greeting()

        # bye
        if self.contains(words, self.byes):
            return self.handle_bye()

        # thanks
        if "thanks" in words:
            return f"Always happy to help, {self.username} 😄"

        # commands
        if "commands" in words or "cmds" in words:
            return self.available_commands()

        # explain command
        if "help" in words or "use" in words or "how" in words:

            command_response = self.explain_command(words)

            if command_response:
                return command_response

        # troubleshooting
        for issue in self.troubleshoot:

            if issue in words:
                return self.diagnose(issue)

        # open apps
        if "open" in words or "run" in words:

            app_response = self.open_app(words)

            if app_response:
                return app_response

        # execute shell commands
        shell_response = self.execute_shell(words)

        if shell_response:
            return shell_response

        # command suggestions
        suggestion = self.suggest_command(text)

        if suggestion:
            return suggestion

        # contextual memory
        context = self.contextual_reply(text)

        if context:
            return context

        # system info
        sysinfo = self.system_info(text)

        if sysinfo:
            return sysinfo

        # fallback
        return (
            "Hmm... I didn't understand that.\n"
            "Try asking about:\n"
            "- commands\n"
            "- wifi\n"
            "- disk\n"
            "- apps\n"
            "- performance"
        )


# main loop
def main(username, args=None):

    pulse = Pulse(username)

    print(f"{pulse.name} {pulse.version} Online...")
    print("Type 'bye' to exit.\n")

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

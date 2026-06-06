![Version](https://img.shields.io/badge/version-v3.2.1-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Status](https://img.shields.io/badge/status-active-success)

# 🚀 PyOS v3.2.1

> A Python-based Operating System Simulator built entirely from scratch.

## 🎬 Demo

![PyOS Demo](screenshots/pyos-demo.gif)

PyOS is a terminal-driven operating system simulator developed using Python. It is designed to explore operating system concepts such as authentication, virtual filesystems, shell environments, security models, logging systems, application runtimes, and user management.

Unlike a real operating system kernel, PyOS runs entirely in user space and focuses on providing a realistic command-line operating system experience for learning, experimentation, and systems design practice.

---

# ✨ Features

## 🔐 Authentication System

* First-boot administrator setup
* Multi-user support
* Secure password hashing with salts
* Hidden password input using `getpass`
* Password validation policies
* Account lockout system after failed login attempts
* Administrative account recovery
* Separate user environments
* Reserved username protection

---

## 📂 Virtual Filesystem

PyOS provides a secure virtual filesystem for each user isolated from the host operating system.

Features:

* Create files
* Delete files
* Read files
* Write files
* Edit files
* Copy files
* Move files
* Rename files
* Create directories
* Delete directories
* Navigate directories
* Display working directory
* List directory contents

### Filesystem Security

* Path traversal protection
* User directory isolation
* Protected system directories
* Protected system files
* Access control enforcement

---

## 🛡️ Security Architecture

PyOS uses a layered and a role-based security model.

### Roles

```text
PyOS
└── Admin
    └── User
```

#### User

Can:

* Access own files
* Run applications
* Modify own data

Cannot:

* Modify system files
* Modify protected directories
* Access other users' data

#### Administrator

Can:

* Manage users
* View system logs
* Access user logs
* Unlock accounts
* Configure system settings

---

### Security Features

* Role-based access control
* Path traversal protection
* Protected system files
* Protected system directories
* User isolation
* Reserved directory protection
* Secure path validation
* Account lock system

---

## 📜 Logging Subsystem

PyOS v3.2.1 introduces a complete logging framework.

### Log Types

#### User Logs

Stored separately for each user.

Tracks:

* Logins
* Logouts
* Command execution
* User errors
* Warnings

#### System Logs

Tracks:

* Boot events
* Shutdown events
* User creation
* Security events
* Critical system operations

#### Backup Logs

Tracks:

* Backup operations
* Restore operations
* Recovery actions

*Reserved for future backup and recovery features.*

---

### Logging Features

* User log viewing
* System log viewing
* Log statistics
* Log trimming
* Automatic log trimming
* Configurable log limits
* Administrative log inspection
* User log management

---

## 💬 Quote Engine

PyOS includes a programming quote engine containing 501 programming and computer science quotes.

Features:

* Random quote generation
* Quote cache system
* No duplicate quotes until all quotes are exhausted
* Automatic cache reset
* Fallback quote protection
* Offline operation

---

## 🎨 Theme Engine

PyOS supports multiple terminal themes.

Built-in terminal themes:

| Theme     | Description          |
| --------- | -------------------- |
| matrix    | Classic hacker green |
| bloodmoon | Dark red danger      |
| ocean     | Aqua blue            |
| royal     | Purple elite         |
| ghost     | Dark mode            |
| sunset    | Yellow-black sunset  |
| ice       | Blue-white           |
| lava      | Red-black            |
| neon      | Magenta-black        |
| default   | Classic terminal     |

Example:

```bash
theme matrix
```

---

# 📦 Built-in Applications

PyOS ships with several bundled applications.

### Calculator

Basic arithmetic calculator.

### Notes

Simple note-taking application.

### Guess

Number guessing game.

### Password Vault

Secure password storage utility.

### Pulse

System utility application.

---


## 🖥️ Shell Environment

PyOS includes:

* Command parser
* Permission-aware command execution
* Virtual path support
* Dynamic app launching
* Session management
* Restart support
* User isolation

Example prompt:

```bash
PyOS:/users/Rohith/home>
```

---

# 📸 Screenshots

### 🔐 Account Lockout Protection

After 5 failed login attempts, PyOS automatically locks the account and requires administrator intervention.

![Account Lockout](screenshots/login-lockout.png)

### 🛡️ Access Control

Protected directories and files cannot be modified by regular users.

![Access Denied](screenshots/accessdenied.png)

### ✏️ Nano-style Text Editor

PyOS includes a lightweight built-in editor supporting file creation and editing.

![Nano Editor](screenshots/edit.png)

#### File Copy

![Copy Command](screenshots/copy.png)

#### File Rename

![Rename Command](screenshots/rename.png)

### 🖥️ Screenfetch

Display system information and version details.

![Screenfetch](screenshots/screenfetch.png)

# 📖 Command Reference

## Utility Commands

| Command     | Description                      |
| ----------- | -------------------------------- |
| help        | Display command help             |
| clear       | Clear terminal                   |
| whoami      | Show current user                |
| date        | Display current date             |
| time        | Display current time             |
| day         | Display current day              |
| uptime      | Display system uptime            |
| pyver       | Display Python version           |
| os          | Display OS information           |
| sysinfo     | Display system information       |
| screenfetch | Display PyOS banner              |
| greet       | Display greeting                 |
| quote       | Display random programming quote |
| mood        | Random mood response             |
| echo        | Echo text                        |
| reverse     | Reverse text                     |
| cal         | Display calendar                 |
| roll        | Roll a dice                      |
| coin        | Flip a coin                      |
| petname     | Generate pet names               |
| whoareu     | About PyOS                       |

---

## User Management Commands

| Command | Description         |
| ------- | ------------------- |
| users   | List users (Admin)  |
| adduser | Create user (Admin) |
| logout  | Logout current user |
| restart | Restart PyOS        |

---

## Application Commands

| Command | Description                 |
| ------- | --------------------------- |
| apps    | List installed applications |
| run     | Launch application          |

---

## Filesystem Commands

| Command | Description             |
| ------- | ----------------------- |
| pwd     | Show current directory  |
| ls      | List directory contents |
| sd      | Change directory        |
| cr      | Create file             |
| del     | Delete file             |
| readf   | Read file               |
| writef  | Write to file           |
| edit    | Open Nano-style editor  |
| copy    | Copy file               |
| move    | Move file               |
| rename  | Rename file             |
| crdir   | Create directory        |
| deldir  | Delete directory        |

---

## Filesystem Commands

### ls

Lists files and directories.

```bash
ls
```

---

### pwd

Displays current directory.

```bash
pwd
```

---

### sd

Changes directory.

```bash
sd <directory>
```

Examples:

```bash
sd Documents
sd ..
sd /
```

---

### cr

Creates a file.

```bash
cr <filename>
```

Examples:

```bash
cr notes
cr notes.txt
```

If no extension is provided, `.txt` is automatically added.

---

### crdir

Creates a directory.

```bash
crdir <directory>
```

---

### del

Deletes a file.

```bash
del <filename>
```

---

### deldir

Deletes an empty directory.

```bash
deldir <directory>
```

---

### readf

Reads a text file.

```bash
readf <filename>
```

Line-number mode:

```bash
readf notes.txt -l
```

---

### writef

Writes text into a file.

```bash
writef <filename> <content>
```

Example:

```bash
writef notes.txt Hello World
```

---

### edit

Built-in Nano-style text editor.

```bash
edit <filename>
```

Editor commands:

```text
:wq   Save and Exit
:q    Exit Without Saving
```

---

### rename

Renames a file or directory.

```bash
rename <old_name> <new_name>
```

---

### copy

Copies a file.

```bash
copy <source> <destination>
```

Example:

```bash
copy notes.txt backup.txt
```

---

### move

Moves a file.

```bash
move <source> <destination>
```

Example:

```bash
move notes.txt archive.txt
```

---

## System Commands

### help

Displays available commands.

```bash
help
```

---

### clear

Clears the terminal.

```bash
clear
```

---

### date

Displays current date.

```bash
date
```

---

### time

Displays current time.

```bash
time
```

---

### day

Displays current day.

```bash
day
```

---

### uptime

Displays system uptime.

```bash
uptime
```

---

### echo

Prints text to the terminal.

```bash
echo Hello World
```

---

### reverse

Reverses text.

```bash
reverse Hello
```

---

### screenfetch

Displays system information.

```bash
screenfetch
```

Version information:

```bash
screenfetch -v
```

---

## User Commands

### whoami

Displays current username.

```bash
whoami
```

---

### users

Lists available users.

```bash
users
```

Administrator only.

---

### adduser

Creates a new user account.

```bash
adduser
```

Administrator only.

---

### petname

Displays the configured assistant name.

```bash
petname
```

---

## Power Commands

### logout

Logs out current user.

```bash
logout
```

---

### restart

Restarts PyOS.

```bash
restart
```

---

### shutdown

Shuts down PyOS.

```bash
shutdown
```

---

## Application Commands

### apps

Lists installed applications.

```bash
apps
```

---

### run

Launches an application.

```bash
run <app_name>
```

Example:

```bash
run calculator
```

---

# 📜 Logging Commands

## User Commands

### Information

```bash
logs info
logs config
logs stats
```

### Viewing Logs

```bash
logs view
logs tail <n>
```

### Management

```bash
logs trim
logs clear
```

### Configuration

```bash
logs set max <value>
logs set trim <on/off>
```

---

## Administrator Commands

### System Logs

```bash
logs system view
logs system tail <n>
logs system stats
logs system info
logs system trim
logs system clear
```

### System Configuration

```bash
logs system set max <value>
logs system set trim <on/off>
```

### User Logs

```bash
logs user <username> view
logs user <username> tail <n>
logs user <username> stats
logs user <username> clear
```

---

# 📂 Filesystem Layout

```text
PyOS/
│
├── apps/
│   ├── calculator.py
│   ├── guess.py
│   ├── notes.py
│   ├── passwordvault.py
│   └── pulse.py
│
├── system/
│   ├── backup/
│   ├── data/
│   │   ├── quotes.json
│   │   └── cache.txt
│   ├── config.json
│   └── log.txt
│
├── users/
│    ├── apps/
│    ├── home/
│    └── system/
│
├── auth.py
├── commands.py
├── fs.py
├── logger.py
├── main.py
├── security.py
└── boot.bat
```

---

# 🛡️ Protected Resources

The following resources cannot be modified by normal users:

### Protected Directories

```text
system/
apps/
home/
```

### Protected Core Files

```text
main.py
auth.py
commands.py
fs.py
security.py
logger.py
boot.bat
```

---

# 📈 Performance

### Boot Time Improvements

| Version | Average Boot Time |
| ------- | ----------------- |
| v3.2.0  | ~23 seconds       |
| v3.2.1  | ~17 seconds       |

Approximately 26% faster boot performance.

---


# ⚙️ Installation

## Requirements

* Python 3.10+
* Windows CMD Terminal

---

## Clone Repository

```bash
git clone https://github.com/r0-vex/PyOS
```

---

## Launch PyOS

Run:

```bash
boot.bat
```

Do not run:

```bash
python main.py
```

PyOS uses a dedicated bootloader process.

---

# 📜 Release Notes

## PyOS v3.2.1

### Added

* Reserved username protection for "PyOS"
* Python version validation during boot
* Quote engine with 501 programming quotes
* Quote cache system
* Complete logging subsystem
* User log management
* System log management
* Log statistics
* Log trimming
* Automatic log trimming
* Configurable log limits
* New data directory

### Improved

* Boot process validation
* Boot performance
* Theme command error handling
* User interface consistency
* Quote reliability
* Command feedback

### Security

* Added logger.py protection
* Improved username validation
* Strengthened system file protection

### Fixed

* Duplicate user creation messages
* Configuration inconsistencies
* Quote cache issues
* Logging edge cases
* Multiple UI/UX issues

---

# 🗺️ Roadmap

## v3.3

* tree command
* find command
* count command
* search command
* manual pages

## v3.4

* Backup system
* Recovery system
* Troubleshooting utilities

## v4.0

* App sandbox
* Package manager
* Application permissions
* Plugin support

---

# ⚠️ Current Limitations

* Windows-focused architecture
* No true multitasking
* No kernel-level isolation
* No app sandboxing yet
* Backup system still in development

---

# 📚 Quote Database Attribution

PyOS includes a programming quote dataset containing quotes from various authors in computer science and software engineering.

All quotes remain the intellectual property of their respective authors.

The dataset is used for educational and non-commercial purposes.

Dataset Source:
[GitHub URL](https://github.com/mudroljub/programming-quotes-api)

---

# 🎓 Educational Purpose

PyOS is NOT a real operating system kernel.

PyOS is:

* An operating system simulator
* A systems programming project
* A shell architecture experiment
* A learning platform for OS concepts
* A practical Python engineering project

---

# 👨‍💻 Developer

Created by **Rohith**.

Built to explore:

* Operating systems
* Filesystem design
* Authentication systems
* Security models
* Command-line environments
* Software architecture

---

# 📄 License

This project is intended for learning, experimentation, and educational use.

---

# 🔥 Final Note

PyOS started as a simple Python terminal project and evolved into a structured operating system simulator featuring:

* Authentication
* Virtual filesystems
* Security controls
* User environments
* Runtime applications
* Logging infrastructure
* Theme support
* Administrative controls

> "Talk is cheap. Show me the code." — Linus Torvalds

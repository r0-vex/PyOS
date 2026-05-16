🚀 PyOS v2.0

> A Python-based terminal operating system simulator built entirely from scratch.



PyOS is a terminal-driven operating system simulator developed using Python. It is designed to simulate core operating system concepts such as authentication, filesystem handling, shell commands, app execution, logging, themes, permissions, and AI-assisted terminal interaction.

PyOS is both:

a learning project for operating system and systems programming concepts

a modular shell ecosystem inspired by real-world terminal environments



---

📌 Features

🔐 Authentication System

First-boot admin setup

User account creation

Login system

Password validation

Password hashing

Role-based permissions

Account lock system after failed attempts

Separate admin and user environments



---

🖥️ Interactive Shell

PyOS provides a terminal-style shell environment.

Example:

PyOS:/home/username>

Supports:

command parsing

command permissions

arguments

app launching

filesystem operations



---

📂 Filesystem Engine

PyOS contains a virtual filesystem layer.

Supported Commands

Command	Description

ls	List files and directories
sd	Change directory
crdir	Create directory
deldir	Delete directory
cr	Create file
del	Delete file
copy	Copy files
rename	Rename files/directories
readf	Read file contents



---

🛡️ Security Features

Username validation

Password validation

Restricted usernames

File extension whitelist

Login attempt limits

User isolation

Protected system directories

Role-based access system



---

📜 Logging System

PyOS includes dynamic logging support.

Available Logs

System logs

User logs

App logs

Backup logs


Example log:

2026-01-31 18:01:43 : INFO : User Logged In


---

🎨 Theme Engine

PyOS supports terminal themes using foreground/background color combinations.

Built-in Themes

matrix

ice

bloodmoon

ocean

royal

terminal

ghost


Example:

color matrix


---

🔄 Power Management

Supported power commands:

Command	Description

shutdown	Exit PyOS
logout	Logout current user
restart	Restart PyOS


PyOS restart system uses:

fresh process launching

batch bootloader

clean shell rebooting



---

🤖 Pulse AI Assistant

Pulse is the built-in AI terminal assistant.

Capabilities:

command help

troubleshooting

app launching

shell assistance

system guidance

PyOS-specific support


Example:

Pulse> Available Commands:


---

🎮 Built-in Apps

Current apps include:

Guess Game

Notes

Calculator

Password Vault

Currency Converter

Pulse AI Assistant


Apps can be launched using:

run appname

Example:

run guess


---

🎲 Guess Game

Features:

Multiple difficulty levels

Hint system

Dynamic scoring

High-score support

Randomized gameplay


Difficulty Modes:

Easy

Hard

Very Hard



---

🧠 Concepts Used

PyOS demonstrates practical implementation of:

OOP

File handling

JSON configuration management

Logging systems

Authentication systems

Password hashing

Runtime app execution

Shell architecture

Virtual filesystem concepts

Error handling

Terminal UI design

Process management

Restart lifecycle management



---

📁 Project Structure

PyOS/
│
├── main.py
├── auth.py
├── commands.py
├── fs.py
├── security.py
├── boot.bat
│
├── system/
│   ├── config.json
│   ├── log.txt
│   └── backup/
│
├── users/
│   └── username/
│       ├── apps/
│       ├── user_files/
│       └── system/
│
└── apps/
    ├── pulse.py
    ├── guess.py
    ├── notes.py
    ├── calculator.py
    └── ...


---

⚙️ Installation

Requirements

Python 3.10+

Windows CMD Terminal



---

Clone Repository

git clone <repository-url>


---

Start PyOS

Run:

boot.bat

Do NOT run:

python main.py

because PyOS uses a dedicated bootloader system.


---

🧩 Configuration

System Configuration

Stored in:

/system/config.json


---

User Configuration

Stored in:

/users/<username>/system/config.json


---

🔧 Future Plans

Planned features include:

Safe mode

Package manager

Background services

Improved Pulse AI

Networking utilities

Process manager

Task scheduler

Plugin system

Custom themes

Script engine

File encryption

Linux support



---

⚠️ Current Limitations

Windows-focused architecture

CMD terminal dependent

No true multitasking yet

No real kernel-level isolation

ANSI support limited



---

💡 Educational Purpose

PyOS is NOT a real operating system kernel.

It is:

an educational operating system simulator

a systems programming practice project

a shell architecture experiment

a terminal ecosystem project



---

👨‍💻 Developer

Developed by Rohith.

Built for:

learning

experimentation

systems design practice

terminal ecosystem development



---

📜 License

This project is open for learning and experimentation.


---

🔥 Final Note

PyOS started as a small Python terminal project and evolved into a modular shell ecosystem featuring:

authentication

filesystem architecture

runtime apps

AI assistance

theme engine

restart lifecycle

logging infrastructure

command parser

virtual user environments


> “Talk is cheap. Show me the code.”

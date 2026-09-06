<div align="center">

<img src="assets/icons/shared_icons/tavana.png" width="120" alt="Tavana logo" />

# Tavana

**Smart Windows Assistant**
A fast and intelligent command launcher for Windows 10 and Windows 11.

![Version](https://img.shields.io/badge/Version-v1.0.0-1f6feb)
![Python](https://img.shields.io/badge/Python-3.14.7-d4a72c)
![License](https://img.shields.io/badge/License-See_Repo-238636)
![Downloads](https://img.shields.io/badge/⭳-Downloads-21262d)

</div>



[English](README.md) |  [فارسی](README_FA.md)

---



<a id="english"></a>

### What is Tavana?

**Tavana** is a smart, fast, and lightweight assistant designed for **Windows 10 and Windows 11**.

It provides a single, simple interface for accessing Windows commands, applications, games, system tools, calculations, and web searches.

Instead of navigating through multiple Windows menus, settings pages, folders, and tools, you can simply open Tavana and tell it what you need.

### ✨ Why Tavana?

Windows provides hundreds of system tools and settings, but finding the right one is not always easy.

Tavana reduces that friction. Instead of asking *"Where is this setting?"*, you can simply type what you need. Tavana searches its command database, identifies the appropriate action, and provides a fast way to execute it.

### ⚡ Quick Access

Tavana is designed to stay out of your way until you need it.

#### Open Tavana

Press:

```
Ctrl + Space
```

The Tavana interface appears instantly and is ready for input. Press the shortcut again when you need to access Tavana.

This makes Tavana suitable for quick, repeated actions without manually searching through the Start Menu or Windows Settings.

### 🧠 What Can Tavana Do?

#### 🪟 Windows Commands

Quickly access Windows tools and system components.

```
Control Panel
Task Manager
Network Connections
Device Manager
Programs and Features
Command Prompt
PowerShell
Windows Settings
```

Tavana can use Windows commands such as:

```
control
ncpa.cpl
appwiz.cpl
cmd
powershell
ms-settings:
```

#### 📁 Find Applications and Games

Tavana can help locate applications and games installed on your computer. Instead of manually searching through directories, enter the application name and Tavana can help you find and launch it.

#### 🧮 Simple Calculator

Tavana can also handle simple mathematical expressions.

```
25 * 18
(120 + 80) / 4
1250 / 5
15 ** 2
```

This allows quick calculations without opening another application.

#### 🔎 Google Search

If your input is not a known Windows command or local application, Tavana can use it as a web search query.

```
How to install Python on Windows
```

Tavana can send the query to Google and open the search results.

#### 🌐 Persian and English Support

Tavana is designed with both **Persian and English users** in mind. Examples of Persian commands:

```
بلوتوث
وای فای
کنترل پنل
مدیریت دستگاه
تنظیمات شبکه
```

The application can recognize and search commands using Persian input.

### 🎯 Designed Like a Command Palette

Tavana follows the idea of a modern **Command Palette**. The workflow is simple:

```
Open Tavana
     ↓
Type what you need
     ↓
Tavana analyzes the input
     ↓
Find the appropriate action
     ↓
Execute or open the result
```

> **Less navigation. More action.**



## User Interface and Themes

### ☀️ Light Mode

<p align="center"><img src="assets/screenshots/light.png" width="850" alt="Tavana light mode screenshot" /></p>

### 🌙 Dark Mode

<p align="center"><img src="assets/screenshots/dark.png" width="850" alt="Tavana dark mode screenshot" /></p>

### 🔥 Key Features

| Feature | Description |
|---|---|
| ⚡ Fast Launcher | Quickly access Windows tools and applications |
| 🪟 Windows Commands | Execute and open useful Windows components |
| 📁 Application Search | Find installed applications and games |
| 🧮 Calculator | Solve simple mathematical expressions |
| 🔎 Google Search | Search the web directly from Tavana |
| 🇮🇷 Persian Support | Search and interact using Persian input |
| 🇬🇧 English Support | Full English interface and commands |
| ⌨️ Global Shortcut | Open Tavana with `Ctrl + Space` |
| 💾 Local Database | Store command data locally |
| 🪶 Lightweight | Designed to remain fast and responsive |
| 🎨 Modern UI | Clean command-palette style interface |

### ⌨️ Keyboard Shortcut

The primary shortcut for Tavana is:

### `Ctrl + Space`

Use it to quickly bring Tavana to the foreground.

```
Ctrl + Space
     ↓
   Tavana
     ↓
Enter your command
     ↓
Select the result
     ↓
   Execute
```

This makes Tavana especially useful for users who prefer keyboard-driven workflows.

### 🔐 Privacy

Privacy is an important part of Tavana's design. The core command database can be stored locally using **SQLite**.

Tavana does not require a remote database for its built-in command information. The local database can contain information such as:

```
Command Name
Windows Command
Category
Description
Icon
Search Keywords
```

Tavana's built-in command data is designed to work locally on the user's computer.

> Internet access may be required for features that intentionally use online services, such as Google Search.

### 🏗️ Architecture

Tavana is designed around a separation between the user interface and the application's core logic.

```
                         Tavana
                            │
              ┌─────────────┴─────────────┐
              │                           │
              Ui                      Core engine
              │                           │
              │              ┌────────────┼────────────┐
              │              │            │            │
              │           Search       Commands    Calculator
              │              │            │            │
              └──────────────┴────────────┴────────────┘
                             │
                       Local Database
                           SQLite
```

This approach makes the project easier to maintain and provides a foundation for future features.

### 💾 Local Database

Tavana uses a local database to manage its command collection. A typical command record can contain:

```
name
command
category
description
icon
keywords
```

This allows the command database to grow without requiring every command to be hard-coded directly into the application.

### 🛠️ Technology Stack

Tavana is built primarily with:

- **Python**
- **PySide6**
- **psutil**
- **Windows APIs / Windows commands**
- **Qt Designer**

#### Runtime

```
Windows 10
Windows 11
```

#### Development

```
Python 3.14.7
PySide6
pywin32
```

> The exact Python version used for each release is specified in the corresponding release information.

### 📦 Installation

#### Option 1 — Download the Release

The easiest way to use Tavana is to download the latest release.

**Latest Release:** [Go to release page](https://github.com/Tavanafzar/Tavana/releases/)

Download the appropriate Windows package and run the installer or executable.

### 🗺️ Roadmap

Tavana is an evolving project. Potential future improvements include:

- [ ] Smarter natural-language command recognition
- [ ] More Windows commands
- [ ] More advanced application discovery
- [ ] Extended Persian command support
- [ ] Plugin system
- [ ] More system automation
- [ ] Improved search ranking
- [ ] Custom user commands
- [ ] Advanced AI capabilities
- [ ] Better personalization
- [ ] Multi-step actions
- [ ] More Windows integrations

The roadmap may change as Tavana develops.

### 🐛 Bug Reports

Found a problem? Please create a GitHub Issue and include:

- Tavana version
- Windows version
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Relevant screenshots
- Error messages or logs

### 💡 Feature Requests

Have an idea for Tavana? Open a Feature Request and describe:

```
What should Tavana do?
Why would this feature be useful?
How should the feature work?
```

Screenshots, examples, and use cases are welcome.

### 📜 License

Tavana is distributed under the license specified in this repository. See: [Read it](LICENSE)

### 👨‍💻 Author

**GitHub — [PARSA MIRI](https://github.com/PARSAMIRI)**

Developer and creator of **Tavana**.

> ⭐ **Star the repository if you like Tavana!**
> If Tavana is useful to you, consider giving the repository a star on GitHub.

---


<div align="center">

**Tavana — Just tell Windows what you need.**

Made with ❤️ by Parsa Miri

</div>

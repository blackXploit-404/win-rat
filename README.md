# Win-Rat
This is a Python-based Telegram bot that allows remote control of a computer via Telegram commands. It provides functionalities like taking screenshots, capturing webcam images, executing system commands, and more. Use this script responsibly and legally, as it includes sensitive features like keylogging and remote system control.

# Features / List of commands ( more staff added later)

/start: Initiates the bot (checks authorization).

/sysinfo: Retrieves system information (IP, hostname, OS, CPU, RAM).

/screenshot: Captures and sends a screenshot.

/webcam: Takes a photo using the webcam.

/shutdown: Shuts down the system.

/restart: Restarts the system.

/lock: Locks the workstation (Windows only).

/cmd <command>: Executes a shell command and returns output.

/download <path>: Sends a file from the system.

/upload: Uploads a file to the system.

/processes: Lists running processes (PID, name, CPU, memory).

/kill <pid>: Terminates a process by PID.

/volume <up/down/mute>: Adjusts system volume (Windows only).

/keylog <start/stop>: Starts/stops a basic keylogger.

/openurl <url>: Opens a URL in the default browser.

/message <text>: Displays a message box (Windows only).

# Prerequisites

Python 3.12 (recommended; Python 3.13 may have compatibility issues with some dependencies).

A Telegram bot token (obtain from @BotFather).

Admin/root privileges for some features (e.g., keylogger).

# Usage

Start a chat with your bot on Telegram.
Send commands (e.g., /sysinfo, /screenshot).

# Example commands:

/screenshot: Takes a screenshot and sends it.

/cmd dir: Runs the dir command (Windows) and returns output.

/keylog start: Starts keylogging; /keylog stop sends captured keys.

# Important Notes

Ethical Use: This bot includes powerful features (e.g., keylogger, remote command execution) that can be misused. Use it only on systems you own or have explicit permission to control. Unauthorized use may violate laws.
Windows-Specific Features: Commands like /lock, /volume, and /message are Windows-only. Non-Windows systems will receive an error message.

# Contributing

Contributions are welcome! Please fork the repository, make changes, and submit a pull request. Ensure your code follows the existing style and includes appropriate checks for cross-platform compatibility.

# Disclaimer
The author is not responsible for any misuse of this software. Use it at your own risk and ensure compliance with all applicable laws and regulations.
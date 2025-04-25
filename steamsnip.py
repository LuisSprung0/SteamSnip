import tkinter as tk
from tkinter import font as tkfont
import subprocess
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def is_steam_blocked():
    cmd = ["netsh", "advfirewall", "firewall", "show", "rule", "name=SteamSnip"]
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return "No rules match" not in result.stdout

def block_steam():
    subprocess.run([
        "netsh", "advfirewall", "firewall", "add", "rule",
        "name=SteamSnip", "dir=out", "action=block",
        "program=C:\\Program Files (x86)\\Steam\\steam.exe"
    ], shell=True)
    update_status()

def unblock_steam():
    subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=SteamSnip"], shell=True)
    update_status()

def update_status():
    blocked = is_steam_blocked()
    status.set("Steam is BLOCKED" if blocked else "Steam is UNBLOCKED")
    color = "#FF5252" if blocked else "#66BB6A"
    status_label.config(fg=color)
    indicator.config(bg=color)

def resize_fonts(event):
    scale = max(0.7, min(2, root.winfo_width() / 350))
    header_font.configure(size=int(20 * scale))
    status_font.configure(size=int(12 * scale))
    button_font.configure(size=int(14 * scale))
    bottom_font.configure(size=int(8 * scale))

root = tk.Tk()
root.iconbitmap("assets/icon.ico")
root.title("SteamSnip")
root.configure(bg="#212121")
root.minsize(600, 400)  
root.geometry("600x400") 

header_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
status_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")
button_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
bottom_font = tkfont.Font(family="Segoe UI", size=8, weight="normal")

status = tk.StringVar(value="Checking status...")

tk.Label(root, text="STEAMSNIP", font=header_font, bg="#212121", fg="#D9D8D7").pack(pady=20)

status_frame = tk.Frame(root, bg="#212121")
status_frame.pack(pady=10)

indicator = tk.Label(status_frame, width=2, bg="#66BB6A")
indicator.pack(side="left", padx=10)

status_label = tk.Label(status_frame, textvariable=status, font=status_font, bg="#212121", fg="white")
status_label.pack(side="left")

btn_frame = tk.Frame(root, bg="#212121")
btn_frame.pack(pady=20, expand=True, fill="both")

def make_btn(text, command, fg):
    btn = tk.Button(
        btn_frame, text=text, command=command, font=button_font,
        bg="#303030", activebackground="#505050", fg=fg, bd=0, relief="flat"
    )
    def on_enter(e): btn.config(bg="#383838")
    def on_leave(e): btn.config(bg="#303030")
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


make_btn("BLOCK", block_steam, "#A97A71").pack(side="left", expand=True, fill="both", padx=10)
make_btn("UNBLOCK", unblock_steam, "#77AA71").pack(side="left", expand=True, fill="both", padx=10)

disclaimer = tk.Label(root, text="*Disclaimer: Needs to run as administrator", font=bottom_font, fg="#D9D8D7", bg="#212121")
disclaimer.pack(side="left", padx=10, pady=10)

license = tk.Label(root, text="Made by: Luis Sprung", font=bottom_font, fg="#D9D8D7", bg="#212121")
license.pack(side="right", padx=10, pady=10)

root.bind("<Configure>", resize_fonts)
update_status()
root.mainloop()

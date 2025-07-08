import json, os, threading,sys
import tkinter as tk
from tkinter import ttk
from login_logic import login_to_portal


CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)


def is_config_valid(config):
    required_keys = ["email", "day", "month", "year", "verification_type", "last_4_digits", "login_link"]
    return all(key in config and config[key] for key in required_keys)

def show_config_window(existing=None):
    def save_and_close():
        config = {
            "email": email_var.get(),
            "day": day_var.get(),
            "month": month_var.get(),
            "year": year_var.get(),
            "verification_type": type_var.get(),
            "last_4_digits": digits_var.get(),
            "login_link": link_var.get()
        }
        save_config(config)
        top.destroy()
        start_login()

    top = tk.Toplevel(root)
    top.title("Enter Details")

    link_var = tk.StringVar(value=existing.get("login_link", "") if existing else "")
    email_var = tk.StringVar(value=existing.get("email", "") if existing else "")
    day_var = tk.StringVar(value=existing.get("day", "") if existing else "")
    month_var = tk.StringVar(value=existing.get("month", "") if existing else "")
    year_var = tk.StringVar(value=existing.get("year", "") if existing else "")
    type_var = tk.StringVar(value=existing.get("verification_type", "") if existing else "")
    digits_var = tk.StringVar(value=existing.get("last_4_digits", "") if existing else "")

    entries = [
        ("Username", email_var),
        ("Day", day_var),
        ("Month", month_var),
        ("Year", year_var),
        ("Verification Type (father/mother)", type_var),
        ("Last 4 Digits", digits_var),
        ("Login Page Link (Contineo)", link_var),
    ]

    for i, (label, var) in enumerate(entries):
        tk.Label(top, text=label).grid(row=i, column=0, pady=2, padx=5, sticky="w")
        tk.Entry(top, textvariable=var).grid(row=i, column=1, pady=2, padx=5)

    tk.Button(top, text="Save", command=save_and_close).grid(row=len(entries), column=0, columnspan=2, pady=10)

def fake_progress(i=0):
    if i <= 100:
        progress_bar["value"] = i
        root.after(30, fake_progress, i+1)

def start_login():
    config = load_config()
    if not config or not is_config_valid(config):
        show_config_window(config or {})
        return

    loading_label.config(text="Launching Chrome...")
    loading_label.pack(pady=(20, 5))
    progress_bar["value"] = 0
    progress_bar.pack()
    fake_progress()

    def threaded_login():
        try:
            driver = login_to_portal(config)
            root.driver_ref = driver 
        except Exception as e:
            root.after(0, lambda: show_config_window(config))
            return
        root.after(0, post_login_success)

    threading.Thread(target=threaded_login).start()

def post_login_success():
    progress_bar.pack_forget()
    loading_label.config(text="Login Successful")
    edit_btn.pack(pady=5)
    exit_btn.pack(pady=5)

    def cleanup_after_delay():
        edit_btn.pack_forget()
        exit_btn.pack_forget()
        loading_label.pack_forget()
        root.withdraw()

    root.after(3000, cleanup_after_delay)

def resource_path(relative_path):
    """ Get absolute path to resource (for PyInstaller compatibility) """
    try:
        base_path = sys._MEIPASS  
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = tk.Tk()
root.title("Crystal Auto Logger")
root.geometry("300x180")
root.resizable(False, False)
root.configure(bg="white")

style = ttk.Style()
style.theme_use("default")
style.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')

loading_label = tk.Label(root, text="", font=("Segoe UI", 10, "italic"), bg="white", fg="#333")
progress_bar = ttk.Progressbar(root, mode='determinate', length=200, style="blue.Horizontal.TProgressbar")

edit_btn = tk.Button(root, text="Edit Details", width=30, command=lambda: show_config_window(load_config()))
exit_btn = tk.Button(root, text="Exit", width=30, command=root.quit)

root.after(100, start_login)
root.iconbitmap(resource_path("app_icon.ico"))
root.after(30*60*1000, root.quit)

root.mainloop()

# Made by HoneyComb

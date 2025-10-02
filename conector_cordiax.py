import os
import sys
import json
import threading
import tkinter as tk
import webbrowser
import requests
from playsound import playsound
import pystray
from PIL import Image, ImageDraw
import time

# ----- Resource Path for PyInstaller compatibility -----
def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ----- Config File with GUI Input -----
CONFIG_FILE = os.path.join(os.path.expanduser("~"), "AjustesConectorCordiax.json")

def load_config():
    config = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
        except:
            pass

    if "topic" not in config or "cordiax_url" not in config:
        root = tk.Tk()
        root.title("Configuración Inicial")
        root.geometry("400x200")
        root.resizable(False, False)

        tk.Label(root, text="Introduce el topic de ntfy.sh:").pack(pady=(20, 5))
        topic_var = tk.StringVar(value=config.get("topic", ""))
        tk.Entry(root, textvariable=topic_var, width=40).pack()

        tk.Label(root, text="Introduce la URL de Cordiax:").pack(pady=(20, 5))
        url_var = tk.StringVar(value=config.get("cordiax_url", ""))
        tk.Entry(root, textvariable=url_var, width=40).pack()

        def save_and_close():
            config["topic"] = topic_var.get().strip()
            config["cordiax_url"] = url_var.get().strip()
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
            root.destroy()

        tk.Button(root, text="Guardar", command=save_and_close).pack(pady=20)
        root.mainloop()

    return config

config = load_config()
TOPIC = config["topic"]
CORDIAX_URL = config["cordiax_url"]
NTFY_URL = f"https://ntfy.sh/{TOPIC}"

# Global Variables
icon = None
popup_offset = 0
popup_lock = threading.Lock()
sound_threads = {}

# High-Priority Sound Loop
def play_sound_loop(popup_id, stop_event):
    while not stop_event.is_set():
        try:
            playsound(resource_path("alarm.wav"), block=False)
        except Exception as e:
            print("Error playing alarm.wav:", e, file=sys.stderr)
        stop_event.wait(10)

# Tray Icon
def create_icon(color):
    image = Image.new('RGB', (64,64), (255,255,255))
    dc = ImageDraw.Draw(image)
    dc.ellipse((16,16,48,48), fill=color)
    return image

def set_tray_status(color, tooltip):
    global icon
    if icon:
        icon.icon = create_icon(color)
        icon.title = tooltip

# Notification Popup
def show_notification(msg, click_url=None, custom_title=None, priority=3):
    global popup_offset, sound_threads
    root = tk.Tk()

    if custom_title:
        root.title(f"Notificación: {custom_title}")
    else:
        root.title("Notificación Cordiax")

    root.geometry("420x220")

    with popup_lock:
        y_offset = 50 + popup_offset
        popup_offset += 40
    root.geometry(f"+100+{y_offset}")

    label = tk.Label(root, text=msg, wraplength=380, justify="center")
    label.pack(pady=20)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    popup_id = id(root)
    stop_event = threading.Event()
    if priority > 3:
        sound_thread = threading.Thread(target=play_sound_loop, args=(popup_id, stop_event), daemon=True)
        sound_thread.start()
        sound_threads[popup_id] = stop_event

    def stop_sound():
        if popup_id in sound_threads:
            sound_threads[popup_id].set()
            del sound_threads[popup_id]

    def on_close():
        stop_sound()
        set_tray_status((200,0,0), "Conectado (esperando)")
        root.destroy()
        with popup_lock:
            nonlocal_y = root.winfo_y()
            if nonlocal_y == popup_offset:
                popup_offset = max(0,popup_offset-40)

    def on_access():
        if click_url:
            webbrowser.open(click_url)
        on_close()

    def on_cordiax():
        webbrowser.open(CORDIAX_URL)
        on_close()

    def on_silenciar():
        stop_sound()

    if click_url:
        acceder_btn = tk.Button(button_frame, text="Acceder", command=on_access)
        acceder_btn.pack(side="left", padx=10)

    aceptar_btn = tk.Button(button_frame, text="Aceptar", command=on_close)
    aceptar_btn.pack(side="left", padx=10)

    cordiax_btn = tk.Button(button_frame, text="Abrir Cordiax", command=on_cordiax)
    cordiax_btn.pack(side="left", padx=10)

    if priority > 3:
        silenciar_btn = tk.Button(button_frame, text="Silenciar", command=on_silenciar)
        silenciar_btn.pack(side="left", padx=10)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

# Listen Ntfy
def listen_ntfy():
    headers = {"Accept":"text/event-stream"}
    while True:
        try:
            set_tray_status((200,0,0), "Conectado (esperando)")
            with requests.get(NTFY_URL, headers=headers, stream=True, timeout=60) as r:
                for line in r.iter_lines():
                    if line and line.startswith(b"data:"):
                        try:
                            data = json.loads(line[5:].decode("utf-8"))
                            msg = data.get("message","")
                            click_url = data.get("click")
                            custom_title = data.get("title")
                            priority = data.get("priority",3)

                            try:
                                playsound(resource_path("ring.wav"), block=False)
                            except:
                                pass

                            set_tray_status((0,200,0), "Nueva notificación")
                            threading.Thread(target=show_notification, args=(msg,click_url,custom_title,priority), daemon=True).start()
                        except Exception as e:
                            print("Error parsing message:", e, file=sys.stderr)
        except Exception as e:
            print("Connection lost:", e, file=sys.stderr)
            set_tray_status((100,180,255), "Desconectado - reintentando...")
            time.sleep(5)

# Start Tray
def start_tray():
    global icon
    def on_exit(icon, item):
        icon.stop()
        sys.exit(0)

    icon = pystray.Icon(
        "conector_cordiax",
        create_icon((200,0,0)),
        "Conector Cordiax",
        menu=pystray.Menu(
            pystray.MenuItem("Salir", on_exit)
        )
    )
    threading.Thread(target=listen_ntfy, daemon=True).start()
    icon.run()

if __name__=="__main__":
    # Prevent console window in onefile GUI mode
    if getattr(sys, 'frozen', False):
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    start_tray()

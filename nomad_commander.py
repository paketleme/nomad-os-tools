import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

# Nomad OS - Master Command Center (V2.2)
# Sistemin beyni: Tüm modülleri tarar ve tek tıkla başlatır.

class NomadCommander:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Master Command Center")
        self.root.geometry("950x750")
        self.root.configure(bg="#1a1b26")
        
        self.colors = {
            "bg": "#1a1b26",
            "sidebar": "#16161e",
            "card": "#24283b",
            "fg": "#c0caf5",
            "accent": "#7aa2f7",
            "green": "#9ece6a",
            "red": "#f7768e",
            "purple": "#bb9af7",
            "orange": "#ff9e64",
            "gray": "#414868"
        }

        # Uygulama Meta Verileri
        self.app_registry = {
            "nomad-ram": ("🧠 RAM Optimizer", "Belleği temizle ve zRAM'i yönet.", self.colors["purple"]),
            "nomad-cleaner": ("🧹 Sistem Temizliği", "Önbelleği ve çöpleri tek tıkla sil.", self.colors["orange"]),
            "nomad-power": ("🔋 Güç Yönetimi", "Pil sağlığı ve enerji profilleri.", self.colors["green"]),
            "nomad-shield": ("🛡️ Nomad Shield", "MAC değişimi, DNS ve veri imha.", self.colors["red"]),
            "nomad-lang": ("🌐 Dil & Klavye", "Global dil arama ve indirme merkezi.", self.colors["accent"]),
            "nomad-pro": ("🎨 Pro Dashboard", "Tema, şifre ve stil ayarları.", self.colors["purple"]),
            "nomad-hub": ("🚀 Uygulama Hub", "Tek tıkla popüler yazılım kurucu.", self.colors["accent"]),
            "nomad-settings": ("⚙️ Ayarlar", "Kullanıcı şifresi ve cihaz adı yönetimi.", self.colors["blue"]),
            "nomad-drivers": ("🔉 Sürücü Merkezi", "Lenovo ses ve donanım onarımı.", self.colors["green"]),
            "nomad-pkg": ("📦 Repo Center", "Bulut senkronizasyonu ve güncelleme.", self.colors["accent"]),
            "pamac-manager": ("🛠️ Paket Mağazası", "Pamac (AUR/Flatpak) Mağazası.", self.colors["red"]),
        }

        self.setup_ui()

    def setup_ui(self):
        # Sol Menü (Sidebar)
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        
        logo_frame = tk.Frame(self.sidebar, bg=self.colors["sidebar"], pady=30)
        logo_frame.pack(fill="x")
        tk.Label(logo_frame, text="🛡️ NOMAD", font=("Sans", 20, "bold"), bg=self.colors["sidebar"], fg=self.colors["accent"]).pack()
        tk.Label(logo_frame, text="STABLE COMMANDER", font=("Sans", 9), bg=self.colors["sidebar"], fg=self.colors["fg"]).pack()

        # Kaydırma Alanı (Canvas)
        self.container = tk.Frame(self.root, bg=self.colors["bg"])
        self.container.pack(side="right", expand=True, fill="both")
        
        self.canvas = tk.Canvas(self.container, bg=self.colors["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors["bg"], padx=30, pady=20)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Başlık
        tk.Label(self.scrollable_frame, text="Sistem Komuta Merkezi", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg="white").pack(anchor="w", pady=(0, 20))

        self.grid_frame = tk.Frame(self.scrollable_frame, bg=self.colors["bg"])
        self.grid_frame.pack(fill="both", expand=True)

        self.refresh_apps()

    def scan_installed_apps(self):
        found_apps = []
        search_dirs = ["/usr/local/bin", "/usr/bin"]
        for d in search_dirs:
            if os.path.exists(d):
                for file in os.listdir(d):
                    if (file.startswith("nomad-") or file == "pamac-manager") and file != "nomad-commander":
                        found_apps.append(file)
        return sorted(list(set(found_apps)))

    def refresh_apps(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        apps = self.scan_installed_apps()
        cols = 3
        for i, app_cmd in enumerate(apps):
            row = i // cols
            col = i % cols
            title, desc, color = self.app_registry.get(app_cmd, (app_cmd.replace("nomad-", "").title(), "Özel Nomad modülü.", self.colors["accent"]))
            self.add_app_card(row, col, title, desc, app_cmd, color)

    def add_app_card(self, r, c, title, desc, command, color):
        card = tk.Frame(self.grid_frame, bg=self.colors["card"], padx=15, pady=15, highlightthickness=1, highlightbackground=self.colors["gray"])
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        
        tk.Label(card, text=title, font=("Sans", 11, "bold"), bg=self.colors["card"], fg=color).pack(anchor="w")
        tk.Label(card, text=desc, font=("Sans", 9), bg=self.colors["card"], fg="#94a3b8", wraplength=180, justify="left").pack(anchor="w", pady=5)
        
        btn = tk.Button(card, text="Başlat", bg=color, fg=self.colors["bg"], font=("Sans", 9, "bold"), relief="flat", command=lambda cmd=command: self.launch_app(cmd))
        btn.pack(side="bottom", fill="x", pady=(10, 0))
        self.grid_frame.grid_columnconfigure(c, weight=1)

    def launch_app(self, cmd):
        def run():
            try:
                process = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                if process.returncode != 0 and stderr:
                    messagebox.showerror("Uygulama Hatası", f"'{cmd}' bir hata ile karşılaştı:\n\n{stderr}")
            except Exception as e:
                messagebox.showerror("Sistem Hatası", f"'{cmd}' başlatılamadı.\n\nHata: {e}")
        
        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadCommander(root)
    tk.Button(root, text="🔄 Listeyi Yenile", bg="#16161e", fg="#7aa2f7", relief="flat", font=("Sans", 8), command=app.refresh_apps).pack(side="bottom", fill="x", pady=5)
    root.mainloop()

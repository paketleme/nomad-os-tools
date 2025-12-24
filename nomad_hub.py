import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

class NomadHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad Hub - Dijital Kontrol Merkezi")
        self.root.geometry("600x700")
        self.root.configure(bg="#1a1b26")

        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#a9b1d6",
            "accent": "#7aa2f7",
            "success": "#9ece6a",
            "warning": "#e0af68",
            "danger": "#f7768e"
        }

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🚀 NOMAD HUB", font=("Sans", 22, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()

        # Notebook (Sekmeli Yapı)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors["card"], foreground=self.colors["fg"], padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", self.colors["accent"])], foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Sekmeleri Oluştur
        self.tab_apps = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.tab_system = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.tab_settings = tk.Frame(self.notebook, bg=self.colors["bg"])

        self.notebook.add(self.tab_apps, text=" 📦 Uygulamalar ")
        self.notebook.add(self.tab_system, text=" ⚙️ Sistem Bakımı ")
        self.notebook.add(self.tab_settings, text=" 🛠️ Hızlı Ayarlar ")

        self.setup_apps_tab()
        self.setup_system_tab()
        self.setup_settings_tab()

    def create_btn(self, parent, text, cmd, color, desc=""):
        frame = tk.Frame(parent, bg=self.colors["card"], pady=10, padx=10)
        frame.pack(fill="x", pady=5)

        btn = tk.Button(frame, text=text, bg=color, fg="white", font=("Sans", 10, "bold"),
                        relief="flat", width=20, command=lambda: threading.Thread(target=cmd).start())
        btn.pack(side="left")

        tk.Label(frame, text=desc, bg=self.colors["card"], fg=self.colors["fg"], font=("Sans", 9, "italic")).pack(side="left", padx=15)

    def setup_apps_tab(self):
        tk.Label(self.tab_apps, text="Tek Tıkla Popüler Yazılımlar", bg=self.colors["bg"], fg=self.colors["accent"], font=("Sans", 11, "bold")).pack(pady=10)
        self.create_btn(self.tab_apps, "Google Chrome", lambda: self.install("google-chrome"), self.colors["accent"], "En popüler web tarayıcısı")
        self.create_btn(self.tab_apps, "VS Code", lambda: self.install("visual-studio-code-bin"), self.colors["accent"], "Profesyonel kod editörü")
        self.create_btn(self.tab_apps, "Discord", lambda: self.install("discord"), self.colors["accent"], "Oyuncu ve topluluk sohbeti")
        self.create_btn(self.tab_apps, "Spotify", lambda: self.install("spotify"), self.colors["accent"], "Müzik ve Podcast")
        self.create_btn(self.tab_apps, "Telegram", lambda: self.install("telegram-desktop"), self.colors["accent"], "Güvenli mesajlaşma")

    def setup_system_tab(self):
        tk.Label(self.tab_system, text="Sistem Sağlığı ve Güncelleme", bg=self.colors["bg"], fg=self.colors["accent"], font=("Sans", 11, "bold")).pack(pady=10)
        self.create_btn(self.tab_system, "Sistemi Güncelle", self.update_sys, self.colors["success"], "Tüm paketleri en yeni sürüme yükseltir")
        self.create_btn(self.tab_system, "Derin Temizlik", self.clean_sys, self.colors["warning"], "Önbelleği ve gereksiz dosyaları siler")
        self.create_btn(self.tab_system, "Disk Analizi", lambda: subprocess.run(["baobab"]), "#565f89", "Hangi dosya ne kadar yer kaplıyor?")
        self.create_btn(self.tab_system, "Sistem İzleyici", lambda: subprocess.run(["xfce4-taskmanager"]), "#565f89", "İşlemci ve RAM kullanımını gör")

    def setup_settings_tab(self):
        tk.Label(self.tab_settings, text="Kullanım Kolaylığı Ayarları", bg=self.colors["bg"], fg=self.colors["accent"], font=("Sans", 11, "bold")).pack(pady=10)
        self.create_btn(self.tab_settings, "Klavye Onar (TR Q)", self.fix_kb, "#565f89", "Klavyeyi anında Türkçe yapar")

        # Gece Işığı Kontrolleri (Geliştirildi)
        night_frame = tk.Frame(self.tab_settings, bg=self.colors["card"], pady=10, padx=10)
        night_frame.pack(fill="x", pady=5)

        tk.Button(night_frame, text="🌙 Gece Işığı AÇ", bg=self.colors["warning"], fg="white", font=("Sans", 10, "bold"),
                  relief="flat", width=15, command=self.night_on).pack(side="left")
        tk.Button(night_frame, text="☀️ KAPAT", bg="#414868", fg="white", font=("Sans", 10, "bold"),
                  relief="flat", width=15, command=self.night_off).pack(side="left", padx=10)

        self.create_btn(self.tab_settings, "Karanlık Mod", self.toggle_dark, "#414868", "Arayüzü karanlık/aydınlık yapar")

    # --- KOMUTLAR ---
    def night_on(self):
        subprocess.run(["redshift", "-O", "4500k"])
        messagebox.showinfo("Gece Işığı", "Göz koruma modu aktif (Sarı ışık).")

    def night_off(self):
        subprocess.run(["redshift", "-x"])
        subprocess.run(["pkill", "redshift"])
        messagebox.showinfo("Gece Işığı", "Ekran renkleri normale döndürüldü.")

    def install(self, pkg):
        messagebox.showinfo("İşlem Başladı", f"{pkg} kuruluyor, lütfen terminale bakın veya bekleyin.")
        subprocess.run(["xfce4-terminal", "-e", f"bash -c 'yay -S --noconfirm {pkg}; read'"])

    def update_sys(self):
        subprocess.run(["xfce4-terminal", "-e", "bash -c 'sudo pacman -Syu --noconfirm; read'"])

    def clean_sys(self):
        subprocess.run(["sudo", "pacman", "-Sc", "--noconfirm"])
        messagebox.showinfo("Başarılı", "Sistem temizlendi!")

    def fix_kb(self):
        subprocess.run(["setxkbmap", "tr"])
        messagebox.showinfo("Klavye", "Klavye Türkçe Q yapıldı.")

    def toggle_dark(self):
        current = subprocess.getoutput("xfconf-query -c xsettings -p /Net/ThemeName")
        new = "Arc" if "Dark" in current else "Arc-Dark"
        subprocess.run(["xfconf-query", "-c", "xsettings", "-p", "/Net/ThemeName", "-s", new])
        subprocess.run(["xfconf-query", "-c", "xsettings", "-p", "/Net/IconThemeName", "-s", "Papirus-Dark"])

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadHub(root)
    root.mainloop()

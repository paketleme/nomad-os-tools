#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

class NomadProDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Pro Dashboard")
        self.root.geometry("600x800")
        self.root.configure(bg="#1a1b26") # Fırtına Mavisi / Siyah
        self.root.resizable(False, False)

        # Tasarım Renk Paleti (Tokyo Night Style)
        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#c0caf5",
            "accent": "#7aa2f7",
            "green": "#9ece6a",
            "red": "#f7768e",
            "orange": "#ff9e64",
            "border": "#414868"
        }

        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Notebook (Sekme) Tasarımı
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=self.colors["card"], 
                        foreground=self.colors["fg"], 
                        padding=[15, 8], 
                        font=("Sans", 10, "bold"))
        style.map("TNotebook.Tab", 
                  background=[("selected", self.colors["accent"])], 
                  foreground=[("selected", "white")])

    def create_widgets(self):
        # --- ÜST PROFİL KARTI ---
        profile_frame = tk.Frame(self.root, bg=self.colors["card"], bd=0)
        profile_frame.pack(fill="x", padx=20, pady=20)
        
        # Kullanıcı İkonu (Emoji)
        tk.Label(profile_frame, text="👤", font=("Sans", 40), 
                 bg=self.colors["card"], fg=self.colors["accent"]).pack(side="left", padx=20, pady=10)
        
        info_inner = tk.Frame(profile_frame, bg=self.colors["card"])
        info_inner.pack(side="left", pady=10)
        
        tk.Label(info_inner, text=os.getlogin().upper(), font=("Sans", 16, "bold"), 
                 bg=self.colors["card"], fg="white").pack(anchor="w")
        tk.Label(info_inner, text="Nomad OS Yetkili Kullanıcı", font=("Sans", 9), 
                 bg=self.colors["card"], fg=self.colors["fg"]).pack(anchor="w")

        # --- ANA SEKMELER ---
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Sekme 1: Kişiselleştirme (Seçme Hakkı)
        self.tab_visual = tk.Frame(self.tabs, bg=self.colors["bg"])
        self.tabs.add(self.tab_visual, text=" 🎨 Stil Seçimi ")

        # Sekme 2: Güvenlik
        self.tab_security = tk.Frame(self.tabs, bg=self.colors["bg"])
        self.tabs.add(self.tab_security, text=" 🔐 Güvenlik ")

        # --- SEKMELERİ DOLDUR ---
        self.setup_visual_tab()
        self.setup_security_tab()

    def setup_visual_tab(self):
        tk.Label(self.tab_visual, text="Sistem Görünümünü Seçin", font=("Sans", 12, "bold"),
                 bg=self.colors["bg"], fg="white").pack(pady=15)

        themes = [
            ("Arc Grey Dark (Önerilen)", "Arc-Grey-Dark", "#4b5262"),
            ("Deep Blue (Karanlık)", "Arc-Dark", "#2f343f"),
            ("Nomad Light (Aydınlık)", "Arc", "#dcdfe4"),
            ("Modern Material", "Materia", "#263238")
        ]

        for name, theme_id, color in themes:
            self.create_theme_card(self.tab_visual, name, theme_id, color)

    def create_theme_card(self, parent, name, theme_id, color_hex):
        card = tk.Frame(parent, bg=self.colors["card"], bd=1, highlightbackground=self.colors["border"], highlightthickness=1)
        card.pack(fill="x", pady=5, padx=20)
        
        # Renk Önizleme Kareciği
        tk.Frame(card, width=20, height=20, bg=color_hex).pack(side="left", padx=10, pady=15)
        
        tk.Label(card, text=name, font=("Sans", 10), bg=self.colors["card"], fg="white").pack(side="left")
        
        tk.Button(card, text="Uygula", bg=self.colors["accent"], fg="white", 
                  relief="flat", font=("Sans", 8, "bold"), padx=10,
                  command=lambda t=theme_id: self.apply_theme(t)).pack(side="right", padx=10)

    def setup_security_tab(self):
        # Şifre Değiştirme Alanı
        container = tk.Frame(self.tab_security, bg=self.colors["bg"], padx=20)
        container.pack(fill="both")

        tk.Label(container, text="Erişim Şifresini Güncelle", font=("Sans", 11, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(pady=15, anchor="w")

        self.old_pass = self.create_modern_input(container, "Mevcut Şifre:", show="*")
        self.new_pass = self.create_modern_input(container, "Yeni Şifre:", show="*")
        
        tk.Button(container, text="Şifreyi Mühürle", bg=self.colors["green"], fg=self.colors["bg"],
                  font=("Sans", 10, "bold"), relief="flat", pady=8,
                  command=self.change_password).pack(fill="x", pady=20)

    def create_modern_input(self, parent, label_text, show=None):
        tk.Label(parent, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"]).pack(anchor="w", pady=(5,0))
        entry = tk.Entry(parent, show=show, bg=self.colors["card"], fg="white", 
                         insertbackground="white", relief="flat", font=("Sans", 11), bd=5)
        entry.pack(fill="x", pady=(5, 10))
        return entry

    # --- AKSİYONLAR ---

    def apply_theme(self, theme_name):
        try:
            subprocess.run(["xfconf-query", "-c", "xsettings", "-p", "/Net/ThemeName", "-s", theme_name])
            # İkonları da otomatik uyduralım
            icon_theme = "Papirus-Dark" if "Dark" in theme_name else "Papirus"
            subprocess.run(["xfconf-query", "-c", "xsettings", "-p", "/Net/IconThemeName", "-s", icon_theme])
            messagebox.showinfo("Başarılı", f"Tema '{theme_name}' olarak değiştirildi!")
        except Exception as e:
            messagebox.showerror("Hata", "Tema uygulanamadı. XFCE ayar motoru bulunamadı.")

    def change_password(self):
        old = self.old_pass.get()
        new = self.new_pass.get()
        
        if not old or not new:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return

        # Mevcut şifre doğrulaması
        check = subprocess.run(['sudo', '-S', '-k', '-v'], input=f"{old}\n", text=True, capture_output=True)
        
        if check.returncode == 0:
            user = os.getlogin()
            proc = subprocess.Popen(['sudo', 'chpasswd'], stdin=subprocess.PIPE, text=True)
            proc.communicate(input=f"{user}:{new}")
            messagebox.showinfo("Başarılı", "Şifreniz başarıyla değiştirildi!")
            self.old_pass.delete(0, tk.END)
            self.new_pass.delete(0, tk.END)
        else:
            messagebox.showerror("Hata", "Mevcut şifre yanlış!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadProDashboard(root)
    root.mainloop()

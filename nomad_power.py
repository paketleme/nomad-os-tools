#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

class NomadPower:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad Power - Enerji Yönetimi")
        self.root.geometry("500x600")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        self.colors = {
            "bg": "#0f172a",
            "card": "#1e293b",
            "fg": "#f8fafc",
            "accent": "#0ea5e9",
            "warning": "#f59e0b",
            "success": "#22c55e",
            "danger": "#ef4444"
        }

        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🔋 NOMAD POWER", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        
        # Ana Konteynır
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=30)
        self.main_frame.pack(fill="both", expand=True)

        # 1. BATARYA DURUMU (Görsel Bar)
        self.status_label = tk.Label(self.main_frame, text="Yükleniyor...", font=("Sans", 12, "bold"),
                                   bg=self.colors["bg"], fg=self.colors["fg"])
        self.status_label.pack(pady=10)

        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

        # 2. AYRINTILI BİLGİLER
        self.info_frame = tk.Frame(self.main_frame, bg=self.colors["card"], pady=15, padx=15)
        self.info_frame.pack(fill="x", pady=20)
        
        self.info_text = tk.Label(self.info_frame, text="Sistem taranıyor...", font=("Monospace", 9),
                                 bg=self.colors["card"], fg="#94a3b8", justify="left")
        self.info_text.pack(anchor="w")

        # 3. GÜÇ MODLARI
        tk.Label(self.main_frame, text="Güç Profilini Seçin", font=("Sans", 11, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(anchor="w", pady=10)

        modes_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        modes_frame.pack(fill="x")

        self.create_mode_btn(modes_frame, "🍃 Tasarruf", self.set_battery_mode, self.colors["success"])
        self.create_mode_btn(modes_frame, "⚖️ Dengeli", self.set_ac_mode, self.colors["accent"])
        self.create_mode_btn(modes_frame, "🚀 Performans", self.set_performance_mode, self.colors["warning"])

        # Alt Bilgi
        tk.Label(self.root, text="Nomad OS - Intelligent Power Management", 
                 bg=self.colors["bg"], fg="#475569", font=("Sans", 8)).pack(side="bottom", pady=10)

    def create_mode_btn(self, parent, text, cmd, color):
        btn = tk.Button(parent, text=text, bg=color, fg="white", font=("Sans", 10, "bold"),
                        relief="flat", width=12, pady=8, command=cmd)
        btn.pack(side="left", padx=5, expand=True)

    # --- AKSİYONLAR VE VERİ ÇEKME ---

    def get_battery_info(self):
        try:
            # upower kullanarak batarya bilgilerini çekiyoruz
            out = subprocess.getoutput("upower -i $(upower -e | grep 'BAT')")
            stats = {}
            for line in out.split('\n'):
                if 'percentage:' in line: stats['percent'] = line.split(':')[1].strip().replace('%', '')
                if 'state:' in line: stats['state'] = line.split(':')[1].strip()
                if 'capacity:' in line: stats['health'] = line.split(':')[1].strip()
            return stats
        except:
            return None

    def update_stats(self):
        stats = self.get_battery_info()
        if stats:
            p = int(stats.get('percent', 0))
            self.progress['value'] = p
            state_tr = "Şarj Oluyor" if stats.get('state') == 'charging' else "Deşarj Oluyor"
            if stats.get('state') == 'fully-charged': state_tr = "Dolu"
            
            self.status_label.config(text=f"%{p} - {state_tr}")
            
            info = f"Sağlık: {stats.get('health', 'Bilinmiyor')}\n"
            info += f"Durum: {stats.get('state', 'Bilinmiyor')}\n"
            info += f"Cihaz: Lenovo IdeaPad Optimized"
            self.info_text.config(text=info)
        
        # Her 30 saniyede bir güncelle
        self.root.after(30000, self.update_stats)

    def set_battery_mode(self):
        subprocess.run(["sudo", "tlp", "bat"])
        messagebox.showinfo("Nomad Power", "Güç tasarruf modu aktif edildi.")

    def set_ac_mode(self):
        subprocess.run(["sudo", "tlp", "ac"])
        messagebox.showinfo("Nomad Power", "Dengeli mod aktif edildi.")

    def set_performance_mode(self):
        # TLP ile tam performans zorlama
        subprocess.run(["sudo", "tlp", "ac"])
        messagebox.showwarning("Nomad Power", "Performans modu aktif. Pil tüketimi artabilir.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadPower(root)
    root.mainloop()

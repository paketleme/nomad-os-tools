#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import psutil
import threading
import time

class NomadRAMBooster:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad RAM Booster")
        self.root.geometry("500x650")
        self.root.configure(bg="#1a1b26")
        self.root.resizable(False, False)

        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#c0caf5",
            "accent": "#bb9af7",
            "green": "#9ece6a",
            "red": "#f7768e",
            "blue": "#7aa2f7"
        }

        self.setup_ui()
        self.update_stats()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🧠 RAM BOOSTER", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=30)
        self.main_frame.pack(fill="both", expand=True)

        # RAM Usage Bar
        tk.Label(self.main_frame, text="Mevcut Bellek Kullanımı", bg=self.colors["bg"], fg=self.colors["fg"]).pack(anchor="w")
        self.usage_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.main_frame, variable=self.usage_var, maximum=100)
        self.progress.pack(fill="x", pady=10)
        
        self.stats_label = tk.Label(self.main_frame, text="Hesaplanıyor...", font=("Monospace", 10),
                                   bg=self.colors["bg"], fg=self.colors["blue"])
        self.stats_label.pack(pady=5)

        # Action Cards
        self.create_action_card("🧹 Derin Temizlik", 
                                "Sistem önbelleğini ve gereksiz RAM bloklarını boşaltır.",
                                self.deep_clean, self.colors["green"])

        self.create_action_card("⚡ zRAM Durumu", 
                                "Sıkıştırılmış bellek teknolojisini kontrol eder.",
                                self.check_zram, self.colors["blue"])

        # Process List Label
        tk.Label(self.main_frame, text="En Çok RAM Tüketenler", font=("Sans", 11, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack(anchor="w", pady=(20, 10))

        # Process Listbox
        self.proc_list = tk.Listbox(self.main_frame, bg=self.colors["card"], fg="white", 
                                   font=("Monospace", 9), borderwidth=0, highlightthickness=0)
        self.proc_list.pack(fill="both", expand=True)

        # Footer
        tk.Label(self.root, text="Nomad OS - Memory Excellence", 
                 bg=self.colors["bg"], fg="#475569", font=("Sans", 8)).pack(side="bottom", pady=10)

    def create_action_card(self, title, desc, cmd, color):
        frame = tk.Frame(self.main_frame, bg=self.colors["card"], pady=10, padx=15)
        frame.pack(fill="x", pady=10)
        
        tk.Label(frame, text=title, font=("Sans", 10, "bold"), bg=self.colors["card"], fg="white").pack(anchor="w")
        tk.Label(frame, text=desc, font=("Sans", 8), bg=self.colors["card"], fg="#94a3b8").pack(anchor="w")
        
        btn = tk.Button(frame, text="Çalıştır", bg=color, fg=self.colors["bg"], 
                        font=("Sans", 8, "bold"), relief="flat", padx=15, command=cmd)
        btn.place(relx=0.8, rely=0.3)

    def update_stats(self):
        mem = psutil.virtual_memory()
        self.usage_var.set(mem.percent)
        self.stats_label.config(text=f"Kullanılan: {mem.used // (1024**2)}MB / Toplam: {mem.total // (1024**2)}MB")
        
        # Update process list
        self.proc_list.delete(0, tk.END)
        procs = sorted(psutil.process_iter(['name', 'memory_percent']), 
                       key=lambda x: x.info['memory_percent'], reverse=True)[:5]
        for p in procs:
            self.proc_list.insert(tk.END, f" {p.info['memory_percent']:.1f}% - {p.info['name']}")

        self.root.after(3000, self.update_stats)

    def deep_clean(self):
        # 1. Sync, 2. Drop Caches (Requires Sudo)
        try:
            cmd = "sync; sudo echo 3 > /proc/sys/vm/drop_caches"
            subprocess.run(['sudo', 'sh', '-c', 'sync; echo 3 > /proc/sys/vm/drop_caches'])
            messagebox.showinfo("Başarılı", "Sistem önbelleği temizlendi ve RAM ferahlatıldı!")
        except:
            messagebox.showerror("Hata", "Yetki hatası! Lütfen sudo şifrenizi terminalden onaylayın.")

    def check_zram(self):
        zram_out = subprocess.getoutput("zramctl")
        if zram_out:
            messagebox.showinfo("zRAM Durumu", zram_out)
        else:
            messagebox.showwarning("zRAM", "zRAM şu an aktif değil. Kurulum scriptini çalıştırın.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadRAMBooster(root)
    root.mainloop()

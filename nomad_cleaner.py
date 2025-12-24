import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

class NomadCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Space Sweeper")
        self.root.geometry("550x700")
        self.root.configure(bg="#1a1b26")
        self.root.resizable(False, False)

        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#c0caf5",
            "accent": "#f7768e",
            "success": "#9ece6a",
            "blue": "#7aa2f7",
            "warning": "#e0af68"
        }

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🧹 SPACE SWEEPER", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        tk.Label(header, text="Sistem Temizliği ve Disk Optimizasyonu", font=("Sans", 10), 
                 bg=self.colors["bg"], fg="#94a3b8").pack()

        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=40)
        self.main_frame.pack(fill="both", expand=True)

        # Temizlik Seçenekleri (Checkboxes)
        self.vars = {
            "pacman": tk.BooleanVar(value=True),
            "orphans": tk.BooleanVar(value=True),
            "cache": tk.BooleanVar(value=True),
            "logs": tk.BooleanVar(value=True),
            "trash": tk.BooleanVar(value=True)
        }

        self.create_check(self.main_frame, "📦 Paket Önbelleği (Pacman Cache)", self.vars["pacman"])
        self.create_check(self.main_frame, "🔗 Yetim Paketler (Gereksiz Bağımlılıklar)", self.vars["orphans"])
        self.create_check(self.main_frame, "📁 Kullanıcı Önbelleği (~/.cache)", self.vars["cache"])
        self.create_check(self.main_frame, "📜 Sistem Günlükleri (Journal Logs)", self.vars["logs"])
        self.create_check(self.main_frame, "🗑️ Çöp Kutusu", self.vars["trash"])

        # İlerleme Çubuğu
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=30)

        # Butonlar
        btn_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=10)

        self.clean_btn = tk.Button(btn_frame, text="🚀 Temizliği Başlat", bg=self.colors["success"], 
                                  fg=self.colors["bg"], font=("Sans", 12, "bold"), 
                                  relief="flat", pady=12, command=self.start_cleaning)
        self.clean_btn.pack(fill="x")

        # Log Alanı
        self.log_text = tk.Text(self.main_frame, height=8, bg="#16161e", fg=self.colors["success"], 
                               font=("Monospace", 9), state="disabled", relief="flat")
        self.log_text.pack(fill="both", pady=20)

        # Footer
        tk.Label(self.root, text="Nomad OS - System Purity", 
                 bg=self.colors["bg"], fg="#475569", font=("Sans", 8)).pack(side="bottom", pady=10)

    def create_check(self, parent, text, var):
        cb = tk.Checkbutton(parent, text=text, variable=var, bg=self.colors["bg"], fg=self.colors["fg"],
                           selectcolor=self.colors["card"], activebackground=self.colors["bg"],
                           activeforeground=self.colors["accent"], font=("Sans", 10))
        cb.pack(anchor="w", pady=5)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_cleaning(self):
        self.clean_btn.config(state="disabled", text="Temizleniyor...")
        self.progress["value"] = 0
        threading.Thread(target=self.run_tasks, daemon=True).start()

    def run_tasks(self):
        tasks = []
        if self.vars["pacman"].get(): tasks.append(("Pacman temizliği", self.clean_pacman))
        if self.vars["orphans"].get(): tasks.append(("Yetim paket temizliği", self.clean_orphans))
        if self.vars["cache"].get(): tasks.append(("Önbellek temizliği", self.clean_cache))
        if self.vars["logs"].get(): tasks.append(("Log temizliği", self.clean_logs))
        if self.vars["trash"].get(): tasks.append(("Çöp kutusu temizliği", self.clean_trash))

        if not tasks:
            self.root.after(0, lambda: messagebox.showwarning("Uyarı", "Lütfen en az bir seçenek belirleyin."))
            self.root.after(0, lambda: self.clean_btn.config(state="normal", text="🚀 Temizliği Başlat"))
            return

        total_tasks = len(tasks)
        for i, (name, func) in enumerate(tasks):
            self.root.after(0, lambda n=name: self.log(f"{n} başlatıldı..."))
            func()
            progress_val = ((i + 1) / total_tasks) * 100
            self.root.after(0, lambda v=progress_val: self.progress.configure(value=v))

        self.root.after(0, self.finish_cleaning)

    # --- TEMİZLİK FONKSİYONLARI ---

    def clean_pacman(self):
        subprocess.run(["sudo", "pacman", "-Sc", "--noconfirm"])
        self.log("Pacman önbelleği boşaltıldı.")

    def clean_orphans(self):
        orphans = subprocess.getoutput("pacman -Qdtq")
        if orphans:
            subprocess.run(f"sudo pacman -Rs {orphans} --noconfirm", shell=True)
            self.log("Gereksiz bağımlılıklar kaldırıldı.")
        else:
            self.log("Yetim paket bulunamadı.")

    def clean_cache(self):
        subprocess.run("rm -rf ~/.cache/*", shell=True)
        self.log("Kullanıcı önbelleği temizlendi.")

    def clean_logs(self):
        subprocess.run(["sudo", "journalctl", "--vacuum-time=1d"])
        self.log("Sistem logları 1 güne daraltıldı.")

    def clean_trash(self):
        subprocess.run("rm -rf ~/.local/share/Trash/*", shell=True)
        self.log("Çöp kutusu boşaltıldı.")

    def finish_cleaning(self):
        self.clean_btn.config(state="normal", text="🚀 Temizliği Başlat")
        messagebox.showinfo("Başarılı", "Nomad OS başarıyla temizlendi ve ferahlatıldı!")
        self.log("TÜM İŞLEMLER TAMAMLANDI.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadCleaner(root)
    root.mainloop()

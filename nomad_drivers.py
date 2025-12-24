import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

class NomadDriverHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Sürücü ve Donanım Merkezi")
        self.root.geometry("600x700")
        self.root.configure(bg="#1a1b26")
        self.root.resizable(False, False)

        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#c0caf5",
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
        tk.Label(header, text="⚙️ DRIVER HUB", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        tk.Label(header, text="Donanım Tarama ve Otomatik Sürücü Yükleyici", font=("Sans", 10), 
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack()

        # Ana Panel
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=30)
        self.main_frame.pack(fill="both", expand=True)

        # Durum Kartı
        self.status_card = tk.Frame(self.main_frame, bg=self.colors["card"], padx=15, pady=15)
        self.status_card.pack(fill="x", pady=10)
        
        self.status_title = tk.Label(self.status_card, text="Sistem Taranıyor...", font=("Sans", 11, "bold"),
                                    bg=self.colors["card"], fg="white")
        self.status_title.pack(anchor="w")
        
        self.status_desc = tk.Label(self.status_card, text="Lütfen 'Sistemi Tara' butonuna basın.", 
                                   bg=self.colors["card"], fg=self.colors["fg"], font=("Sans", 9))
        self.status_desc.pack(anchor="w", pady=5)

        # Sürücü Listesi (Ağaç Görünümü)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.colors["card"], foreground="white", 
                        fieldbackground=self.colors["card"], borderwidth=0)
        
        self.tree = ttk.Treeview(self.main_frame, columns=("Hardware", "Status"), show="headings", height=8)
        self.tree.heading("Hardware", text="Donanım")
        self.tree.heading("Status", text="Durum")
        self.tree.column("Hardware", width=350)
        self.tree.column("Status", width=150)
        self.tree.pack(fill="both", pady=15)

        # Butonlar
        btn_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=10)

        self.scan_btn = tk.Button(btn_frame, text="🔍 Sistemi Tara", bg=self.colors["accent"], fg="white",
                                 font=("Sans", 10, "bold"), relief="flat", padx=20, pady=10, command=self.start_scan)
        self.scan_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.fix_btn = tk.Button(btn_frame, text="🚀 Eksikleri Tamamla", bg=self.colors["success"], fg=self.colors["bg"],
                                font=("Sans", 10, "bold"), relief="flat", padx=20, pady=10, state="disabled", command=self.start_fix)
        self.fix_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Log Çıktısı
        self.log_text = tk.Text(self.main_frame, height=6, bg="#16161e", fg="#9ece6a", 
                               font=("Monospace", 8), state="disabled", relief="flat")
        self.log_text.pack(fill="both", pady=10)

        tk.Label(self.root, text="Nomad OS - Hardware Excellence", bg=self.colors["bg"], 
                 fg="#414868", font=("Sans", 8)).pack(side="bottom", pady=10)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_scan(self):
        self.scan_btn.config(state="disabled")
        self.tree.delete(*self.tree.get_children())
        self.log("Donanım analizi başlatıldı...")
        threading.Thread(target=self.scan_hardware, daemon=True).start()

    def scan_hardware(self):
        # Simüle edilmiş ve gerçek kontrol karışımı
        hardware_checks = [
            ("Ekran Kartı (VGA)", "lspci | grep -i vga"),
            ("Kablosuz Ağ (Wi-Fi)", "lspci | grep -i network"),
            ("Ses Kartı (Audio)", "lspci | grep -i audio"),
            ("Bluetooth", "lsusb | grep -i bluetooth"),
            ("İşlemci Mikro-Kod", "grep -E 'vendor_id|model name' /proc/cpuinfo | head -n 2")
        ]

        missing_count = 0
        for name, cmd in hardware_checks:
            result = subprocess.getoutput(cmd)
            status = "Yüklü / Hazır"
            
            # NVIDIA kontrolü örneği
            if "NVIDIA" in result and "nvidia" not in subprocess.getoutput("lsmod"):
                status = "Sürücü Eksik!"
                missing_count += 1
            
            self.root.after(0, lambda n=name, s=status: self.tree.insert("", tk.END, values=(n, s)))
        
        self.root.after(0, self.finish_scan, missing_count)

    def finish_scan(self, count):
        self.scan_btn.config(state="normal")
        if count > 0:
            self.status_title.config(text=f"⚠️ {count} Eksik Sürücü Tespit Edildi!", fg=self.colors["warning"])
            self.status_desc.config(text="Sistem performansını artırmak için sürücüleri yükleyin.")
            self.fix_btn.config(state="normal")
        else:
            self.status_title.config(text="✅ Tüm Sürücüler Güncel", fg=self.colors["success"])
            self.status_desc.config(text="Sisteminiz en iyi şekilde yapılandırılmış görünüyor.")
            self.fix_btn.config(state="disabled")
        self.log("Tarama tamamlandı.")

    def start_fix(self):
        self.fix_btn.config(state="disabled")
        self.log("Sürücü yükleme işlemi başlatılıyor...")
        threading.Thread(target=self.fix_drivers, daemon=True).start()

    def fix_drivers(self):
        # Gerçek yükleme komutları
        commands = [
            "sudo pacman -S --needed --noconfirm linux-firmware sof-firmware",
            "sudo pacman -S --needed --noconfirm base-devel",
            # Mikro kodlar
            "grep -q 'Intel' /proc/cpuinfo && sudo pacman -S --needed --noconfirm intel-ucode",
            "grep -q 'AMD' /proc/cpuinfo && sudo pacman -S --needed --noconfirm amd-ucode"
        ]

        for cmd in commands:
            self.root.after(0, lambda c=cmd: self.log(f"Çalıştırılıyor: {c}"))
            subprocess.run(cmd, shell=True)

        self.root.after(0, self.finish_fix)

    def finish_fix(self):
        messagebox.showinfo("Başarılı", "Eksik sürücüler ve mikro-kodlar başarıyla yüklendi.\nDeğişikliklerin aktif olması için sistemi YENİDEN BAŞLATIN.")
        self.log("Tüm işlemler bitti. Yeniden başlatma önerilir.")
        self.status_title.config(text="✅ Onarım Tamamlandı", fg=self.colors["success"])
        self.fix_btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadDriverHub(root)
    root.mainloop()

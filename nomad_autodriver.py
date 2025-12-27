#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

# =================================================================
# NOMAD OS - AUTO-DRIVER & CLEANER (V1.2 - AGGRESSIVE CLEANUP)
# =================================================================
# Bu modül; kurulumdan önce eski çakışmaları siler, veritabanı 
# kilitlerini kırar ve sistemi yeni sürücüler için sterilize eder.
# =================================================================

class NomadAutoDriver:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Akıllı Kurulum Asistanı")
        self.root.geometry("700x850")
        self.root.configure(bg="#1a1b26")
        self.root.resizable(False, False)

        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "accent": "#7aa2f7",
            "green": "#9ece6a",
            "red": "#f7768e",
            "fg": "#c0caf5",
            "yellow": "#e0af68"
        }

        self.setup_ui()
        threading.Thread(target=self.scan_hardware, daemon=True).start()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=30)
        header.pack(fill="x")
        tk.Label(header, text="🛡️ NOMAD AUTO-DRIVER", font=("Sans", 24, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        tk.Label(header, text="Eskiler süpürülüyor, donanım mühürleniyor...", font=("Sans", 10), 
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack()

        # Ana Panel
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=40)
        self.main_frame.pack(fill="both", expand=True)

        # Tespit Listesi
        tk.Label(self.main_frame, text="📍 Donanım ve Çakışma Analizi:", font=("Sans", 11, "bold"),
                 bg=self.colors["bg"], fg="white").pack(anchor="w", pady=(10, 5))
        
        self.hw_list = tk.Text(self.main_frame, height=12, bg="#16161e", fg=self.colors["green"],
                              font=("Monospace", 9), padx=10, pady=10, relief="flat")
        self.hw_list.pack(fill="x", pady=5)

        # İlerleme Çubuğu
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.main_frame, variable=self.progress_var, maximum=100)
        self.progress.pack(fill="x", pady=20)

        # Durum
        self.status_label = tk.Label(self.main_frame, text="Analiz ediliyor...", bg=self.colors["bg"], fg=self.colors["fg"])
        self.status_label.pack()

        # Alt Butonlar
        self.btn_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        self.btn_frame.pack(side="bottom", fill="x", pady=30)

        self.install_btn = tk.Button(self.btn_frame, text="🚀 ESKİLERİ SİL VE MÜHÜRLE", state="disabled",
                                    bg=self.colors["green"], fg=self.colors["bg"], font=("Sans", 12, "bold"),
                                    relief="flat", pady=15, command=self.start_installation)
        self.install_btn.pack(fill="x")

    def log_hw(self, text, color="green"):
        self.hw_list.tag_config("red", foreground=self.colors["red"])
        self.hw_list.tag_config("green", foreground=self.colors["green"])
        self.hw_list.tag_config("yellow", foreground=self.colors["yellow"])
        
        tag = "green" if color == "green" else ("red" if color == "red" else "yellow")
        self.hw_list.insert(tk.END, f"• {text}\n", tag)
        self.hw_list.see(tk.END)

    def scan_hardware(self):
        self.hw_list.delete("1.0", tk.END)
        packages_to_install = ["base-devel", "networkmanager", "pipewire-pulse"]
        self.conflicts_to_remove = []

        # 1. Paket Veritabanı Kontrolü
        if os.path.exists("/var/lib/pacman/db.lck"):
            self.log_hw("HATA: Veritabanı kilitli! (Otomatik çözülecek)", "red")

        # 2. Ses Çakışma Analizi (JACK2 vs PipeWire)
        check_jack = subprocess.getoutput("pacman -Qs jack2")
        if check_jack:
            self.log_hw("ÇAKIŞMA: jack2 tespit edildi. (Silinecek)", "red")
            self.conflicts_to_remove.append("jack2")

        # 3. GPU Tarama
        gpu_info = subprocess.getoutput("lspci | grep -i vga")
        if "Intel" in gpu_info:
            self.log_hw("Ekran Kartı: Intel (Garantili Mod)", "green")
            packages_to_install += ["xf86-video-intel", "mesa", "intel-media-driver"]
        elif "NVIDIA" in gpu_info:
            self.log_hw("Ekran Kartı: NVIDIA (Güçlü Mod)", "green")
            packages_to_install += ["nvidia", "nvidia-utils"]
        
        # 4. Lenovo Ses Fix Kontrolü
        self.log_hw("Ses: Lenovo Intel SST Fix Hazırlanıyor", "yellow")
        packages_to_install += ["sof-firmware", "alsa-ucm-conf", "pipewire-jack"]

        self.needed_pkgs = list(set(packages_to_install))
        self.status_label.config(text="Analiz bitti. Eskiler silinip yeniler mühürlenecek.")
        self.install_btn.config(state="normal")
        self.progress_var.set(100)

    def start_installation(self):
        self.install_btn.config(state="disabled", text="OPERASYON SÜRÜYOR...")
        threading.Thread(target=self.run_provisioning, daemon=True).start()

    def run_provisioning(self):
        try:
            # ADIM 1: Kilitleri Kır
            subprocess.run("sudo rm -f /var/lib/pacman/db.lck", shell=True)
            subprocess.run("sudo killall -9 pacman pamac-manager 2>/dev/null", shell=True)

            # ADIM 2: Eskileri Kaldır (Çakışan paketler)
            if self.conflicts_to_remove:
                conflicts = " ".join(self.conflicts_to_remove)
                subprocess.run(f"sudo pacman -Rdd {conflicts} --noconfirm", shell=True)

            # ADIM 3: Yenileri Mühürle
            pkgs = " ".join(self.needed_pkgs)
            cmd = f"xfce4-terminal --title='Nomad Provisioning' -e \"bash -c 'sudo pacman -Syu --needed --noconfirm {pkgs}; read -p İşlem bitti, kapatmak için Enter...'\""
            subprocess.run(cmd, shell=True)
            
            # ADIM 4: Lenovo Cerrahi Müdahale
            subprocess.run("echo 'options snd-intel-dspcfg dsp_driver=3' | sudo tee /etc/modprobe.d/nomad.conf", shell=True)
            
            # Eski hatalı configleri temizle
            subprocess.run("sudo rm -f /etc/modprobe.d/alsa-base.conf 2>/dev/null", shell=True)
            
            self.root.after(0, self.finish_setup)
        except Exception as e:
            messagebox.showerror("Hata", f"Operasyon başarısız: {e}")

    def finish_setup(self):
        messagebox.showinfo("Mühürlendi", "Eski çakışmalar silindi ve güncel sürücüler mühürlendi!\n\nDeğişikliklerin aktif olması için sistem yeniden başlatılacak.")
        subprocess.run(["sudo", "reboot"])

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadAutoDriver(root)
    root.mainloop()

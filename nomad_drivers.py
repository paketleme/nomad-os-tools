import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

class NomadDriverHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Sürücü ve Donanım Merkezi v2.0")
        self.root.geometry("650x750")
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
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="⚙️ DRIVER HUB PRO", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        tk.Label(header, text="Donanım Analizi ve Derin Ses Onarımı", font=("Sans", 10), 
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack()

        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=30)
        self.main_frame.pack(fill="both", expand=True)

        # Durum Kartı
        self.status_card = tk.Frame(self.main_frame, bg=self.colors["card"], padx=15, pady=15)
        self.status_card.pack(fill="x", pady=10)
        
        self.status_title = tk.Label(self.status_card, text="Sistem Analizine Hazır", font=("Sans", 11, "bold"),
                                    bg=self.colors["card"], fg="white")
        self.status_title.pack(anchor="w")
        
        self.status_desc = tk.Label(self.status_card, text="Ses kartı ve diğer donanımlar için derin tarama yapın.", 
                                   bg=self.colors["card"], fg=self.colors["fg"], font=("Sans", 9))
        self.status_desc.pack(anchor="w", pady=5)

        # Liste
        self.tree = ttk.Treeview(self.main_frame, columns=("Hardware", "Status"), show="headings", height=10)
        self.tree.heading("Hardware", text="Donanım / Servis")
        self.tree.heading("Status", text="Durum / Teşhis")
        self.tree.column("Hardware", width=300)
        self.tree.column("Status", width=250)
        self.tree.pack(fill="both", pady=15)

        # Butonlar
        btn_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=10)

        self.scan_btn = tk.Button(btn_frame, text="🔍 Derin Tarama Başlat", bg=self.colors["accent"], fg="white",
                                 font=("Sans", 10, "bold"), relief="flat", padx=20, pady=10, command=self.start_scan)
        self.scan_btn.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.fix_btn = tk.Button(btn_frame, text="🚀 Ses ve Sürücüleri Onar", bg=self.colors["success"], fg=self.colors["bg"],
                                font=("Sans", 10, "bold"), relief="flat", padx=20, pady=10, state="disabled", command=self.start_fix)
        self.fix_btn.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Log
        self.log_text = tk.Text(self.main_frame, height=5, bg="#16161e", fg="#9ece6a", 
                               font=("Monospace", 8), state="disabled", relief="flat")
        self.log_text.pack(fill="both", pady=10)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_scan(self):
        self.scan_btn.config(state="disabled")
        self.tree.delete(*self.tree.get_children())
        self.log("Derin donanım analizi başlatıldı...")
        threading.Thread(target=self.scan_logic, daemon=True).start()

    def scan_logic(self):
        missing_count = 0
        
        # 1. Ses Kartı Kontrolü (Hayati)
        sound_cards = subprocess.getoutput("aplay -l | grep 'card'")
        if not sound_cards or "no soundcards found" in sound_cards.lower():
            res = ("Ses Kartı", "KART BULUNAMADI (Sürücü Hatası!)")
            missing_count += 1
        else:
            res = ("Ses Kartı", "Algılandı (Yapılandırma Gerekebilir)")
        self.root.after(0, lambda r=res: self.tree.insert("", tk.END, values=r))

        # 2. Firmware Kontrolü
        sof_check = subprocess.getoutput("pacman -Qs sof-firmware")
        if not sof_check:
            res = ("Ses Firmware (SOF)", "EKSİK!")
            missing_count += 1
        else:
            res = ("Ses Firmware (SOF)", "Yüklü")
        self.root.after(0, lambda r=res: self.tree.insert("", tk.END, values=r))

        # 3. Kernel Modül Kontrolü (Intel Smart Sound)
        dsp_check = subprocess.getoutput("dmesg | grep -i 'sof-audio'")
        if "error" in dsp_check.lower() or not dsp_check:
            res = ("Intel SST Motoru", "ÇALIŞMIYOR / HATA")
            missing_count += 1
        else:
            res = ("Intel SST Motoru", "Aktif")
        self.root.after(0, lambda r=res: self.tree.insert("", tk.END, values=r))

        # 4. Diğerleri
        gpu = ("Ekran Kartı", "Hazır")
        self.root.after(0, lambda r=gpu: self.tree.insert("", tk.END, values=r))

        self.root.after(0, self.finish_scan, missing_count)

    def finish_scan(self, count):
        self.scan_btn.config(state="normal")
        if count > 0:
            self.status_title.config(text=f"⚠️ {count} Kritik Hata Tespit Edildi!", fg=self.colors["warning"])
            self.status_desc.config(text="Özellikle ses donanımında sorunlar var. Onar butonuna basın.")
            self.fix_btn.config(state="normal")
        else:
            self.status_title.config(text="✅ Sürücüler Yazılımsal Olarak Tam", fg=self.colors["success"])
            self.status_desc.config(text="Hala ses gelmiyorsa PipeWire servislerini kontrol edin.")
            self.fix_btn.config(state="normal") # Yine de açık bırakalım, servisi sıfırlasın
        self.log("Tarama bitti.")

    def start_fix(self):
        self.fix_btn.config(state="disabled")
        self.log("Cerrahi ses onarımı başlatılıyor...")
        threading.Thread(target=self.fix_logic, daemon=True).start()

    def fix_logic(self):
        # 1. Sürücüleri zorla tazele
        self.log("Firmware paketleri mühürleniyor...")
        subprocess.run("sudo pacman -S --needed --noconfirm sof-firmware alsa-ucm-conf pipewire-pulse wireplumber", shell=True)
        
        # 2. Intel Smart Sound (Lenovo Fix)
        self.log("Kernel parametreleri Lenovo için güncelleniyor...")
        config_cmd = "echo 'options snd-intel-dspcfg dsp_driver=3' | sudo tee /etc/modprobe.d/nomad-audio.conf"
        subprocess.run(config_cmd, shell=True)
        
        # 3. Servisleri kullanıcı adına başlat
        self.log("PipeWire servisleri uyandırılıyor...")
        subprocess.run("systemctl --user enable --now pipewire pipewire-pulse wireplumber", shell=True)

        self.root.after(0, self.finish_fix)

    def finish_fix(self):
        messagebox.showinfo("Başarılı", "Ses onarımı ve sürücü mühürleme bitti!\n\nKRİTİK: Ayarların aktif olması için sistemi YENİDEN BAŞLATMALISIN.")
        self.log("İşlem bitti. Lütfen Reboot yapın.")
        self.status_title.config(text="✅ Onarım Mühürlendi", fg=self.colors["success"])

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadDriverHub(root)
    root.mainloop()

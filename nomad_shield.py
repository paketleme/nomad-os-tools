import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import subprocess
import os
import threading

class NomadShield:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad Shield - Gizlilik ve Güvenlik")
        self.root.geometry("550x650")
        self.root.configure(bg="#0f172a") # Koyu Lacivert/Siyah (Security Theme)
        self.root.resizable(False, False)

        self.colors = {
            "bg": "#0f172a",
            "card": "#1e293b",
            "fg": "#f8fafc",
            "accent": "#38bdf8",
            "danger": "#ef4444",
            "success": "#22c55e",
            "warning": "#f59e0b"
        }

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🛡️ NOMAD SHIELD", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        tk.Label(header, text="Gizlilik ve İz Bırakmama Modülü", font=("Sans", 10), 
                 bg=self.colors["bg"], fg="#94a3b8").pack()

        main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=30)
        main_frame.pack(fill="both", expand=True)

        # 1. MAC ADRESİ RANDOMİZER
        self.create_section(main_frame, "📡 Ağ Gizliliği (MAC Changer)", 
                          "Ağ kartının fiziksel adresini rastgele değiştirir.",
                          "MAC Adresini Değiştir", self.colors["accent"], self.change_mac)

        # 2. DNS GÜVENLİĞİ
        self.create_section(main_frame, "🌍 Güvenli DNS", 
                          "İnternet trafiğini Cloudflare (1.1.1.1) üzerinden korur.",
                          "Güvenli DNS Uygula", self.colors["success"], self.set_dns)

        # 3. METADATA TEMİZLEYİCİ
        self.create_section(main_frame, "📁 Metadata Temizleyici", 
                          "Dosyaların içindeki gizli (konum, saat vb.) bilgileri siler.",
                          "Dosya Seç ve Temizle", self.colors["warning"], self.clean_metadata)

        # 4. GÜVENLİ SİLME
        self.create_section(main_frame, "🚮 Veri İmha (Secure Shred)", 
                          "Dosyayı geri getirilemez şekilde kalıcı olarak yok eder.",
                          "Dosyayı Güvenli Sil", self.colors["danger"], self.secure_delete)

        # Footer
        tk.Label(self.root, text="Nomad OS - Stealth Mode Active", 
                 bg=self.colors["bg"], fg="#475569", font=("Sans", 8)).pack(side="bottom", pady=10)

    def create_section(self, parent, title, desc, btn_text, btn_color, command):
        frame = tk.Frame(parent, bg=self.colors["card"], pady=12, padx=15)
        frame.pack(fill="x", pady=8)
        
        tk.Label(frame, text=title, font=("Sans", 11, "bold"), 
                 bg=self.colors["card"], fg=self.colors["fg"]).pack(anchor="w")
        tk.Label(frame, text=desc, font=("Sans", 9), 
                 bg=self.colors["card"], fg="#94a3b8").pack(anchor="w", pady=(0, 10))
        
        btn = tk.Button(frame, text=btn_text, bg=btn_color, fg="white", 
                        font=("Sans", 9, "bold"), relief="flat", cursor="hand2",
                        command=lambda: threading.Thread(target=command).start())
        btn.pack(fill="x")

    # --- AKSİYONLAR ---

    def change_mac(self):
        # macchanger yüklü olmalı
        interface = subprocess.getoutput("ip route | grep default | awk '{print $5}'")
        if interface:
            subprocess.run(["sudo", "ip", "link", "set", interface, "down"])
            result = subprocess.run(["sudo", "macchanger", "-r", interface], capture_output=True, text=True)
            subprocess.run(["sudo", "ip", "link", "set", interface, "up"])
            if result.returncode == 0:
                messagebox.showinfo("Başarılı", f"Yeni MAC adresi atandı!\nArayüz: {interface}")
            else:
                messagebox.showerror("Hata", "Macchanger yüklü değil veya hata oluştu.\nKurmak için: sudo pacman -S macchanger")
        else:
            messagebox.showerror("Hata", "Aktif ağ arayüzü bulunamadı.")

    def set_dns(self):
        dns_content = "nameserver 1.1.1.1\nnameserver 1.0.0.1"
        try:
            process = subprocess.Popen(['sudo', 'tee', '/etc/resolv.conf'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=dns_content)
            messagebox.showinfo("Başarılı", "Cloudflare DNS ayarlandı.")
        except:
            messagebox.showerror("Hata", "DNS ayarları güncellenemedi.")

    def clean_metadata(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # mat2 metadata temizleme aracı kullanılır
            result = subprocess.run(["mat2", file_path], capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Başarılı", "Metadata temizlendi! (.cleaned uzantılı dosya oluşturuldu)")
            else:
                messagebox.showerror("Hata", "MAT2 aracı yüklü değil.\nKurmak için: sudo pacman -S mat2")

    def secure_delete(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if messagebox.askyesno("Onay", "BU DOSYA GERİ GETİRİLEMEZ! Silmek istediğine emin misin?"):
                # shred komutu veriyi 3 kez rastgele veriyle ezer
                subprocess.run(["shred", "-u", "-n", "3", "-z", file_path])
                messagebox.showinfo("Başarılı", "Dosya güvenli bir şekilde imha edildi.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadShield(root)
    root.mainloop()

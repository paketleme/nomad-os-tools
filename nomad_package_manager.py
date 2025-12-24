import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading
import requests

# Nomad Repo Center (V2.1)
# Bulut senkronizasyonu ve kendi kendini güncelleme modülü.
# Bu araç, GitHub üzerinden diğer tüm Nomad modüllerini çekmek için kullanılır.

class NomadPkgManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Uzak Depo ve Paket Merkezi")
        self.root.geometry("750x880")
        self.root.configure(bg="#1a1b26")
        
        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#c0caf5",
            "accent": "#7aa2f7",
            "green": "#9ece6a",
            "red": "#f7768e",
            "yellow": "#e0af68",
            "gray": "#414868"
        }

        # --- [ GITHUB REPO AYARI ] ---
        # Buradaki URL'yi kendi GitHub kullanıcı adınla güncellemeyi unutma!
        self.REPO_URL = "https://raw.githubusercontent.com/paketleme/nomad-os-tools/main/"
        
        # Sistemdeki komut isimleri ve GitHub'daki dosya isimleri eşleşmesi
        self.nomad_tools = {
            "nomad-commander": "nomad_commander.py",
            "nomad-shield": "nomad_shield.py",
            "nomad-ram": "nomad_ram_booster.py",
            "nomad-power": "nomad_power.py",
            "nomad-lang": "nomad_language_switcher.py",
            "nomad-pro": "nomad_pro_dashboard.py",
            "nomad-settings": "nomad_user_settings.py",
            "nomad-drivers": "nomad_drivers.py",
            "nomad-cleaner": "nomad_cleaner.py",
            "nomad-hub": "nomad_hub.py",
            "nomad-pkg": "nomad_package_manager.py"
        }

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="📦 NOMAD REPO CENTER", font=("Sans", 22, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)

        self.cloud_tab = tk.Frame(self.tabs, bg=self.colors["bg"])
        self.tabs.add(self.cloud_tab, text=" ☁️ Bulut Senkronizasyonu ")

        self.setup_cloud_tab()

    def setup_cloud_tab(self):
        # Araçları Güncelleme Kartı
        cloud_card = tk.Frame(self.cloud_tab, bg=self.colors["card"], padx=15, pady=15)
        cloud_card.pack(fill="x", pady=10)
        
        tk.Label(cloud_card, text="Nomad Araçlarını Güncelle", font=("Sans", 11, "bold"), 
                 bg=self.colors["card"], fg="white").pack(anchor="w")
        
        tk.Button(cloud_card, text="🔄 Tüm Araçları Bulutla Eşitle", bg=self.colors["green"], 
                  fg=self.colors["bg"], relief="flat", font=("Sans", 10, "bold"),
                  command=self.start_cloud_sync).pack(fill="x", pady=10)

        # Kendi Kendini Güncelleme Kartı
        self_update_card = tk.Frame(self.cloud_tab, bg=self.colors["card"], padx=15, pady=15)
        self_update_card.pack(fill="x", pady=5)
        
        tk.Label(self_update_card, text="Repo Center Güncelleme", font=("Sans", 11, "bold"), 
                 bg=self.colors["card"], fg=self.colors["yellow"]).pack(anchor="w")
        
        tk.Button(self_update_card, text="⚡ Repo Center'ı Şimdi Güncelle", bg=self.colors["accent"], 
                  fg="white", relief="flat", font=("Sans", 10, "bold"),
                  command=self.start_self_update).pack(fill="x", pady=10)

        # Log Ekranı
        self.log_text = tk.Text(self.cloud_tab, height=12, bg="#16161e", fg=self.colors["green"], font=("Monospace", 9))
        self.log_text.pack(fill="both", expand=True, pady=10)

    def log(self, message):
        self.log_text.insert(tk.END, f"> {message}\n")
        self.log_text.see(tk.END)

    def start_cloud_sync(self):
        if messagebox.askyesno("Onay", "Tüm modüller GitHub üzerinden güncellenecek. Devam edilsin mi?"):
            self.log_text.delete("1.0", tk.END)
            threading.Thread(target=self.sync_logic, daemon=True).start()

    def start_self_update(self):
        if messagebox.askyesno("Repo Güncelleme", "Repo Center (Bu uygulama) güncellenecek. Devam edilsin mi?"):
            self.log_text.delete("1.0", tk.END)
            threading.Thread(target=self.self_update_logic, daemon=True).start()

    def sync_logic(self):
        self.log("Bulut sunucusuna bağlanılıyor...")
        success_count = 0
        # Kendisi hariç diğer araçları güncelle
        tools_to_sync = {k: v for k, v in self.nomad_tools.items() if k != "nomad-pkg"}
        for tool_cmd, file_name in tools_to_sync.items():
            if self.download_and_install(tool_cmd, file_name):
                success_count += 1
        self.log(f"\nOperasyon bitti. {success_count} araç güncellendi.")
        messagebox.showinfo("Bitti", "Nomad OS modülleri başarıyla güncellendi!")

    def self_update_logic(self):
        self.log("Repo Center güncelleniyor...")
        if self.download_and_install("nomad-pkg", "nomad_package_manager.py"):
            self.log("Repo Center başarıyla güncellendi!")
            messagebox.showinfo("Başarılı", "Repo Center güncellendi! Lütfen uygulamayı kapatıp tekrar açın.")
        else:
            self.log("Repo Center güncellemesi başarısız oldu.")

    def download_and_install(self, cmd_name, file_name):
        try:
            url = f"{self.REPO_URL}{file_name}"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                temp_file = f"/tmp/{file_name}"
                with open(temp_file, "w") as f: 
                    f.write(response.text)
                
                # Sistem dizinine mühürleme işlemi
                dest = f"/usr/local/bin/{cmd_name}"
                subprocess.run(["sudo", "cp", temp_file, dest])
                subprocess.run(["sudo", "chmod", "+x", dest])
                # Python yolunu (shebang) garantiye alıyoruz
                subprocess.run(["sudo", "sed", "-i", "1i #!/usr/bin/python3", dest])
                # Eğer ikinci bir shebang varsa siliyoruz
                subprocess.run(["sudo", "sed", "-i", "2{/#!/d}", dest])
                
                self.log(f"TAMAMLANDI: {cmd_name}")
                return True
            else:
                self.log(f"HATA: {cmd_name} indirilemedi (HTTP {response.status_code})")
                return False
        except Exception as e:
            self.log(f"SİSTEM HATASI ({cmd_name}): {str(e)}")
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadPkgManager(root)
    root.mainloop()

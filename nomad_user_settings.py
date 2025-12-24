import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os

class NomadControlCenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Kontrol Merkezi")
        self.root.geometry("500x750")
        self.root.configure(bg="#1a1b26") # Nomad Dark Theme (Tokyo Night Style)
        self.root.resizable(False, False)

        # Tasarım Renk Paleti
        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#a9b1d6",
            "accent": "#7aa2f7",
            "success": "#9ece6a",
            "warning": "#e0af68",
            "danger": "#f7768e",
            "border": "#414868"
        }

        self.setup_ui()

    def setup_ui(self):
        # Üst Başlık (Header)
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🛡️ NOMAD OS CENTER", font=("Sans", 20, "bold"), 
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()
        tk.Label(header, text="Dijital Özgürlük - Yönetim Paneli", font=("Sans", 10, "italic"), 
                 bg=self.colors["bg"], fg=self.colors["fg"]).pack()

        # Ana İçerik Alanı
        main_frame = tk.Frame(self.root, bg=self.colors["bg"], padx=30)
        main_frame.pack(fill="both", expand=True)

        # --- 1. KULLANICI GÜVENLİĞİ (ŞİFRE) ---
        self.create_section_label(main_frame, "🔐 Kullanıcı Güvenliği")
        
        self.current_pass_entry = self.create_input(main_frame, "Mevcut Şifre:", show="*")
        self.pass_entry = self.create_input(main_frame, "Yeni Şifre:", show="*")
        self.pass_confirm = self.create_input(main_frame, "Yeni Şifre Tekrar:", show="*")
        
        self.create_button(main_frame, "Şifreyi Güncelle", self.colors["accent"], self.change_password)

        self.add_separator(main_frame)

        # --- 2. SİSTEM KİMLİĞİ (HOSTNAME) ---
        self.create_section_label(main_frame, "🖥️ Sistem Kimliği")
        self.host_entry = self.create_input(main_frame, "Yeni Cihaz Adı (örn: Nomad-X):")
        self.create_button(main_frame, "İsmi Güncelle", self.colors["success"], self.change_hostname)

        self.add_separator(main_frame)

        # --- 3. HIZLI ARAÇLAR ---
        self.create_section_label(main_frame, "🛠️ Hızlı Onarım Araçları")
        
        btn_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        btn_frame.pack(fill="x", pady=5)

        self.create_button(btn_frame, "🧹 Temizlik", self.colors["warning"], self.run_cleaner, side="left", width=18)
        self.create_button(btn_frame, "⌨️ Klavye Onar", "#565f89", self.fix_keyboard, side="right", width=18)

        # Alt Bilgi (Footer)
        footer_text = f"Aktif Kullanıcı: {os.getlogin().upper()}"
        footer = tk.Label(self.root, text=footer_text, bg=self.colors["bg"], fg="#414868", font=("Sans", 8))
        footer.pack(side="bottom", pady=10)

    # --- ARAYÜZ YARDIMCILARI ---

    def create_section_label(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Sans", 12, "bold"), 
                       bg=self.colors["bg"], fg=self.colors["accent"])
        lbl.pack(anchor="w", pady=(15, 5))

    def create_input(self, parent, label_text, show=None):
        tk.Label(parent, text=label_text, bg=self.colors["bg"], fg=self.colors["fg"], font=("Sans", 9)).pack(anchor="w")
        entry = tk.Entry(parent, show=show, bg=self.colors["card"], fg="white", 
                        insertbackground="white", relief="flat", font=("Sans", 10), bd=5)
        entry.pack(fill="x", pady=(0, 10))
        return entry

    def create_button(self, parent, text, color, command, side=None, width=None):
        btn = tk.Button(parent, text=text, bg=color, fg="white" if color != self.colors["success"] else "#1a1b26", 
                        font=("Sans", 10, "bold"), relief="flat", cursor="hand2", command=command, width=width)
        if side:
            btn.pack(side=side, pady=10, padx=2)
        else:
            btn.pack(fill="x", pady=10)
        return btn

    def add_separator(self, parent):
        sep = tk.Frame(parent, height=1, bg=self.colors["border"])
        sep.pack(fill="x", pady=15)

    # --- AKSİYONLAR ---

    def verify_current_password(self, password):
        """Sudo üzerinden şifre doğrulaması yapar."""
        try:
            # -S: Stdin'den oku, -k: Önceki izinleri unut, -v: Doğrula
            check_cmd = subprocess.run(
                ['sudo', '-S', '-k', '-v'],
                input=f"{password}\n",
                text=True,
                capture_output=True
            )
            return check_cmd.returncode == 0
        except:
            return False

    def change_password(self):
        current_p = self.current_pass_entry.get()
        p1 = self.pass_entry.get()
        p2 = self.pass_confirm.get()

        if not current_p or not p1 or not p2:
            messagebox.showwarning("Uyarı", "Tüm alanları doldurmalısın!")
            return

        if p1 != p2:
            messagebox.showerror("Hata", "Yeni şifreler eşleşmiyor!")
            return

        if not self.verify_current_password(current_p):
            messagebox.showerror("Hata", "Mevcut şifren yanlış!")
            return

        try:
            user = os.getlogin()
            proc = subprocess.Popen(['sudo', 'chpasswd'], stdin=subprocess.PIPE, text=True)
            proc.communicate(input=f"{user}:{p1}")
            
            if proc.returncode == 0:
                messagebox.showinfo("Başarılı", "Şifren başarıyla güncellendi!")
                self.current_pass_entry.delete(0, tk.END)
                self.pass_entry.delete(0, tk.END)
                self.pass_confirm.delete(0, tk.END)
            else:
                messagebox.showerror("Hata", "Şifre değiştirilirken bir hata oluştu.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def change_hostname(self):
        new_h = self.host_entry.get()
        if new_h:
            subprocess.run(['sudo', 'hostnamectl', 'set-hostname', new_h])
            messagebox.showinfo("Başarılı", f"Cihaz adı '{new_h}' yapıldı.\nDeğişiklik için sistemi yeniden başlatın.")
            self.host_entry.delete(0, tk.END)

    def run_cleaner(self):
        if messagebox.askyesno("Sistem Temizliği", "Pacman önbelleği ve loglar temizlenecek. Onaylıyor musun?"):
            subprocess.run(['sudo', 'pacman', '-Sc', '--noconfirm'])
            subprocess.run(['sudo', 'journalctl', '--vacuum-time=1d'])
            messagebox.showinfo("Tamamlandı", "Sistem ferahlatıldı!")

    def fix_keyboard(self):
        # Hem anlık hem kalıcı onarım
        subprocess.run(['setxkbmap', 'tr'])
        subprocess.run(['sudo', 'localectl', 'set-x11-keymap', 'tr'])
        messagebox.showinfo("Onarıldı", "Klavye düzeni Türkçe Q olarak mühürlendi!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadControlCenter(root)
    root.mainloop()

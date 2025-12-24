#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import os
import threading

class NomadLanguageHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Nomad OS - Akıllı Dil ve Bölge Merkezi")
        self.root.geometry("550x720")
        self.root.configure(bg="#1a1b26")
        self.root.resizable(False, False)

        self.colors = {
            "bg": "#1a1b26",
            "card": "#24283b",
            "fg": "#c0caf5",
            "accent": "#bb9af7",
            "success": "#9ece6a",
            "blue": "#7aa2f7",
            "warning": "#e0af68"
        }

        # Dil kodlarını klavye düzenleriyle eşleştiren akıllı tablo
        self.layout_map = {
            'tr': 'tr',
            'en': 'us',
            'de': 'de',
            'fr': 'fr',
            'es': 'es',
            'it': 'it',
            'ru': 'ru',
            'az': 'tr' # Azerice için genelde TR klavye kullanılır
        }

        self.active_locales = self.get_active_locales()
        self.all_supported = self.get_all_supported_locales()

        self.setup_ui()

    def get_active_locales(self):
        try:
            output = subprocess.getoutput("localectl list-locales")
            locales = [l.strip() for l in output.split('\n') if l.strip()]
            return sorted(list(set(locales)))
        except:
            return ["tr_TR.UTF-8", "en_US.UTF-8"]

    def get_all_supported_locales(self):
        try:
            output = subprocess.getoutput("grep 'UTF-8' /usr/share/i18n/SUPPORTED | cut -d' ' -f1")
            return sorted(list(set(output.split('\n'))))
        except:
            return ["tr_TR.UTF-8", "en_US.UTF-8"]

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["bg"], pady=20)
        header.pack(fill="x")
        tk.Label(header, text="🌐 NOMAD LANGUAGE HUB PRO", font=("Sans", 18, "bold"),
                 bg=self.colors["bg"], fg=self.colors["accent"]).pack()

        self.main_container = tk.Frame(self.root, bg=self.colors["bg"], padx=35)
        self.main_container.pack(fill="both", expand=True)

        # --- SEÇİM ALANI ---
        self.section_label("📍 Aktif Sistem Dili", self.colors["blue"])

        self.lang_combo = ttk.Combobox(self.main_container, values=self.active_locales, state="readonly")
        current_lang = subprocess.getoutput("echo $LANG")
        if current_lang in self.active_locales:
            self.lang_combo.set(current_lang)
        else:
            self.lang_combo.current(0) if self.active_locales else None
        self.lang_combo.pack(fill="x", pady=5)

        tk.Button(self.main_container, text="Seçili Dili ve Uygun Klavyeyi Uygula", bg=self.colors["blue"], fg="white",
                  font=("Sans", 9, "bold"), relief="flat", pady=8,
                  command=lambda: self.apply_language(self.lang_combo.get())).pack(fill="x", pady=10)

        tk.Button(self.main_container, text="🔍 Yeni Dil Ara ve İndir", bg=self.colors["card"], fg=self.colors["fg"],
                  font=("Sans", 9), relief="flat", pady=5, borderwidth=1, highlightthickness=1,
                  command=self.open_search_window).pack(fill="x", pady=5)

        self.add_separator()

        # --- KLAVYE DÜZENİ ---
        self.section_label("⌨️ Manuel Klavye Ayarı", self.colors["success"])

        self.kb_layouts = [("Türkçe Q", "tr"), ("English US", "us"), ("German", "de"), ("French", "fr")]
        self.kb_combo = ttk.Combobox(self.main_container, values=[k[0] for k in self.kb_layouts], state="readonly")
        self.kb_combo.current(0)
        self.kb_combo.pack(fill="x", pady=5)

        tk.Button(self.main_container, text="Sadece Klavyeyi Değiştir", bg=self.colors["success"], fg=self.colors["bg"],
                  font=("Sans", 9, "bold"), relief="flat", pady=8,
                  command=lambda: self.apply_keyboard_manual(self.kb_layouts[self.kb_combo.current()][1])).pack(fill="x", pady=10)

        # Footer
        tk.Label(self.root, text="Nomad OS - Smart Localization v3.1",
                 bg=self.colors["bg"], fg="#475569", font=("Sans", 8)).pack(side="bottom", pady=10)

    def section_label(self, text, color):
        tk.Label(self.main_container, text=text, font=("Sans", 11, "bold"),
                 bg=self.colors["bg"], fg=color).pack(anchor="w", pady=(15, 5))

    def add_separator(self):
        tk.Frame(self.main_container, height=1, bg="#414868").pack(fill="x", pady=20)

    # --- AKILLI KLAVYE EŞLEŞTİRME ---
    def auto_match_keyboard(self, locale_code):
        """Dil koduna bakarak klavyeyi tahmin eder."""
        lang_prefix = locale_code.split('_')[0].lower()
        matched_layout = self.layout_map.get(lang_prefix)

        if matched_layout:
            # Kullanıcıya soralım mı?
            msg = f"Sistem dili {locale_code} yapılıyor.\nKlavyeyi de otomatik olarak '{matched_layout.upper()}' düzenine çekelim mi?"
            if messagebox.askyesno("Akıllı Klavye Eşleşmesi", msg):
                self.apply_keyboard_logic(matched_layout)

    # --- ARAMA PENCERESİ ---
    def open_search_window(self):
        self.search_win = tk.Toplevel(self.root)
        self.search_win.title("Dil Arama ve İndirme")
        self.search_win.geometry("500x600")
        self.search_win.configure(bg="#1a1b26")
        self.search_win.transient(self.root)
        self.search_win.grab_set()

        tk.Label(self.search_win, text="🌍 Global Dil Kütüphanesi", font=("Sans", 14, "bold"),
                 bg="#1a1b26", fg=self.colors["blue"]).pack(pady=15)

        search_var = tk.StringVar()
        search_var.trace("w", lambda *args: self.filter_search(search_var.get()))
        entry = tk.Entry(self.search_win, textvariable=search_var, bg=self.colors["card"], fg="white",
                         insertbackground="white", relief="flat", font=("Sans", 11))
        entry.pack(fill="x", padx=30, ipady=5)

        list_frame = tk.Frame(self.search_win, bg="#1a1b26")
        list_frame.pack(fill="both", expand=True, padx=30, pady=15)

        self.search_listbox = tk.Listbox(list_frame, bg=self.colors["card"], fg=self.colors["fg"],
                                         selectbackground=self.colors["accent"], borderwidth=0, font=("Monospace", 10))
        self.search_listbox.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(list_frame)
        sb.pack(side="right", fill="y")
        self.search_listbox.config(yscrollcommand=sb.set)
        sb.config(command=self.search_listbox.yview)

        self.btn_download = tk.Button(self.search_win, text="İndir ve Aktif Et", bg=self.colors["success"],
                                      font=("Sans", 10, "bold"), relief="flat", pady=10,
                                      command=self.start_download_thread)
        self.btn_download.pack(fill="x", padx=30, pady=20)

        self.filter_search("")

    def filter_search(self, term):
        self.search_listbox.delete(0, tk.END)
        for loc in self.all_supported:
            if term.lower() in loc.lower():
                self.search_listbox.insert(tk.END, loc)

    def start_download_thread(self):
        selection = self.search_listbox.get(tk.ACTIVE)
        if selection:
            self.btn_download.config(state="disabled", text="İndiriliyor... Lütfen Bekleyin")
            threading.Thread(target=self.download_and_apply, args=(selection,), daemon=True).start()

    def download_and_apply(self, code):
        try:
            subprocess.run(f"sudo sed -i 's/^#\\({code}\\)/\\1/' /etc/locale.gen", shell=True)
            check = subprocess.run(f"grep -q '^{code}' /etc/locale.gen", shell=True)
            if check.returncode != 0:
                subprocess.run(f"echo '{code} UTF-8' | sudo tee -a /etc/locale.gen", shell=True)

            subprocess.run("sudo locale-gen", shell=True)
            self.apply_language_logic(code)
            self.root.after(0, lambda: self.on_download_complete(code))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))

    def on_download_complete(self, code):
        self.search_win.destroy()
        self.active_locales = self.get_active_locales()
        self.lang_combo.config(values=self.active_locales)
        self.lang_combo.set(code)

        # OTOMATİK KLAVYE SORGUSU
        self.auto_match_keyboard(code)

        messagebox.showinfo("Başarılı", f"{code} dili indirildi.\nSistem dili ve (onay verdiyseniz) klavye güncellendi.")

    # --- GENEL AKSİYONLAR ---
    def apply_language(self, code):
        if messagebox.askyesno("Onay", f"Sistem dili {code} olarak değiştirilecek. Devam edilsin mi?"):
            self.apply_language_logic(code)
            # KLAVYE EŞLEŞTİRME
            self.auto_match_keyboard(code)
            messagebox.showinfo("Başarılı", "Dil ayarları güncellendi.")

    def apply_language_logic(self, code):
        subprocess.run(f"sudo localectl set-locale LANG={code}", shell=True)
        subprocess.run(f"xfconf-query -c xsettings -p /Gtk/Locale -n -t string -s {code}", shell=True)

    def apply_keyboard_manual(self, layout):
        self.apply_keyboard_logic(layout)
        messagebox.showinfo("Klavye", f"Klavye '{layout.upper()}' düzenine ayarlandı.")

    def apply_keyboard_logic(self, layout):
        subprocess.run(f"setxkbmap {layout}", shell=True)
        subprocess.run(f"sudo localectl set-x11-keymap {layout}", shell=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = NomadLanguageHub(root)
    root.mainloop()

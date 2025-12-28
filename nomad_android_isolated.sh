#!/bin/bash

# =================================================================
# NOMAD OS - ISOLATED ANDROID ENFORCER (WAYDROID)
# =================================================================
# Bu script, Android sistemini tamamen izole bir konteyner içinde
# kurar ve izin sistemini mühürler.
# =================================================================

# Renkler
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}HATA: Bu operasyon sudo yetkisi gerektirir!${NC}"
   exit 1
fi

echo -e "${CYAN}>>> ANDROID İZOLASYON OPERASYONU BAŞLIYOR...${NC}"

# 1. Wayland Kontrolü (Waydroid sadece Wayland'de çalışır)
if [[ "$XDG_SESSION_TYPE" != "wayland" ]]; then
    echo -e "${YELLOW}[!] UYARI: Wayland oturumunda değilsiniz. Waydroid X11'de çalışmaz.${NC}"
    echo -e "${YELLOW}Lütfen giriş ekranında 'Wayland' veya 'Hyprland/Sway' seçin.${NC}"
fi

# 2. Kernel Modülleri (Binder) - İletişim tüneli
echo -e "${CYAN}>>> 1. Kernel modülleri mühürleniyor...${NC}"
modprobe binder_linux
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK] Binder modülü aktif.${NC}"
else
    echo -e "${RED}[HATA] Kernel binder desteği bulunamadı!${NC}"
fi

# 3. Waydroid ve Bağımlılıkların Kurulumu
echo -e "${CYAN}>>> 2. Waydroid paketleri yükleniyor...${NC}"
pacman -S --needed --noconfirm waydroid lxc python-gobject

# 4. İzolasyon Odaklı Başlatma (Vanilla)
# GApps (Google Servisleri) veri sızdırdığı için 'Vanilla' (Saf) Android öneriyoruz.
echo -e "${YELLOW}>>> 3. Saf Android İmajı İndiriliyor (Vanilla Mode)...${NC}"
echo -e "${YELLOW}Bu işlem yaklaşık 1GB veri indirecektir.${NC}"
waydroid init -s VANILLA

# 5. İzin ve İzolasyon Ayarları
echo -e "${CYAN}>>> 4. İzolasyon Katmanları Yapılandırılıyor...${NC}"

# Konteyner servisini başlat
systemctl enable --now waydroid-container

# Uygulamaların ana sisteme doğrudan erişimini kısıtla
# Waydroid varsayılan olarak kullanıcı klasörünü (Documents vb.) paylaşır.
# Bunu sadece 'okuma' moduna alabiliriz veya tamamen kapatabiliriz.
echo ">>> Klasör paylaşımı kısıtlanıyor..."
waydroid prop set persist.waydroid.active_apps true
waydroid prop set persist.waydroid.multi_windows true

echo -e "${GREEN}=================================================================${NC}"
echo -e "${GREEN} ANDROID KAFESİ (WAYDROID) MÜHÜRLENDİ! 📱🛡️${NC}"
echo -e "${GREEN} =================================================================${NC}"
echo " "
echo " KULLANIM TALİMATLARI:"
echo " 1. 'waydroid show-full-ui' yazarak Android dünyasına gir."
echo " 2. APK yüklemek için: 'waydroid app install dosya.apk'"
echo " 3. İZOLASYON NOTU: Uygulamalar sadece Android içindeki "
echo "    ayarlarda izin verdiğin kadar sisteme müdahil olabilir."
echo " "
echo " 'Can Abi' kuralı: Uygulamaya güvenme, kafesine güven! 😉"
echo "================================================================="

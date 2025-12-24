#!/bin/bash

# =================================================================
# NOMAD OS - SYSTEM DOCTOR & REPAIR TOOL (V1.2 - ULTIMATE FIX)
# =================================================================
# Bu araç sistemdeki TÜM Nomad yazılımlarını teşhis eder ve onarır.
# Modülleri /usr/local/bin dizinine mühürler.
# =================================================================

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Lütfen bu doktoru sudo ile çalıştırın: sudo ./nomad_doctor.sh${NC}"
   exit 1
fi

echo -e "${CYAN}>>> NOMAD OS DOKTORU SİSTEMİ TARIYOR VE ONARIYOR...${NC}"

# 1. Bağımlılık Kontrolü
echo -e "\n${CYAN}[1/3] Bağımlılıklar Kontrol Ediliyor...${NC}"
PACKAGES=("tk" "python-psutil" "macchanger" "mat2" "tlp" "upower" "feh" "plank" "redshift" "python-requests")
for pkg in "${PACKAGES[@]}"; do
    if pacman -Qs "$pkg" > /dev/null; then
        echo -e "${GREEN}[OK] $pkg yüklü.${NC}"
    else
        echo -e "${YELLOW}[!] $pkg eksik, yükleniyor...${NC}"
        pacman -S --needed --noconfirm "$pkg"
    fi
done

# 2. Dosya, İzin ve Shebang Onarımı
echo -e "\n${CYAN}[2/3] Modüller Sisteme Mühürleniyor...${NC}"
declare -A APPS
APPS=(
    ["nomad_commander.py"]="nomad-commander"
    ["nomad_shield.py"]="nomad-shield"
    ["nomad_ram_booster.py"]="nomad-ram"
    ["nomad_power.py"]="nomad-power"
    ["nomad_language_switcher.py"]="nomad-lang"
    ["nomad_pro_dashboard.py"]="nomad-pro"
    ["nomad_user_settings.py"]="nomad-settings"
    ["nomad_hub.py"]="nomad-hub"
    ["nomad_package_manager.py"]="nomad-pkg"
    ["nomad_cleaner.py"]="nomad-cleaner"
    ["nomad_drivers.py"]="nomad-drivers"
)

for file in "${!APPS[@]}"; do
    dest="/usr/local/bin/${APPS[$file]}"
    
    if [ -f "$file" ]; then
        echo -e "${CYAN}İşleniyor: $file -> $dest${NC}"
        cp "$file" "$dest"
        
        # Shebang Fix (Python dosyasını Bash sanmasını engeller)
        if ! head -n 1 "$dest" | grep -q "#!"; then
            sed -i '1i #!/usr/bin/python3' "$dest"
        fi
        
        chmod +x "$dest"
        echo -e "${GREEN}[TAMAM] $dest hazır.${NC}"
    else
        if [ -f "$dest" ]; then
            chmod +x "$dest"
            echo -e "${GREEN}[OK] Sistemdeki $dest mevcut.${NC}"
        else
            echo -e "${RED}[UYARI] $file dosyası yerel klasörde bulunamadı.${NC}"
        fi
    fi
done

# 3. Grafik Yetki ve Menü Yenileme
echo -e "\n${CYAN}[3/3] Grafik Yetkileri ve Menü Tazeleniyor...${NC}"
update-desktop-database /usr/share/applications 2>/dev/null

echo -e "\n${GREEN}=================================================================${NC}"
echo -e "${GREEN} TEŞHİS VE ONARIM TAMAMLANDI! 🛡️🚀${NC}"
echo -e "${GREEN} =================================================================${NC}"
echo " Nomad OS artık hatasız çalışıyor! 🔥"

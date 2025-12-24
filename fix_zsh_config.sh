#!/bin/bash

# =================================================================
# NOMAD OS - ZSH CONFIG REPAIR (V1.6)
# =================================================================
# .zshrc dosyasını onarır ve sisteme 'nomad-zsh-fix' adıyla gömer.
# =================================================================

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

# Kendi kendini sisteme yükleme ve mühürleme
if [[ "$0" != "/usr/local/bin/nomad-zsh-fix" ]]; then
    sudo cp "$0" /usr/local/bin/nomad-zsh-fix
    sudo chmod +x /usr/local/bin/nomad-zsh-fix
fi

echo -e "${CYAN}>>> .zshrc temizleniyor ve p10k ayarları mühürleniyor...${NC}"

# Temiz ve optimize edilmiş .zshrc içeriği oluşturuluyor
cat <<'EOF' > ~/.zshrc
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh 2>/dev/null

# Nomad OS Özel Kısayolları (Aliases)
alias cls="clear"
alias update="sudo pacman -Syu"
alias nomad="fastfetch"

# Powerlevel10k ve Fastfetch entegrasyonu
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
[ -f /usr/bin/fastfetch ] && fastfetch
EOF

echo -e "${GREEN}ZSH AYARLARI ONARILDI VE MÜHÜRLENDİ! 🔥${NC}"

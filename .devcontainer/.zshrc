# Oh My Zsh Configuration
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"
ENABLE_CORRECTION="true"

plugins=(
    git
    git-auto-fetch
    uv
    zsh-autosuggestions
    zsh-syntax-highlighting
)

zstyle ':omz:plugins:pipenv' auto-shell no
source $ZSH/oh-my-zsh.sh

eval "$(starship init zsh)"

# Local paths for a build. Fonts (Poppins, Manrope as TTF, Anton, Great Vibes), lucide icons and the closing track are
# not in the repository: put them in ../assets/ (see ../README.md for where each comes from) or point these at them.
B=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
export MTG_FONTS=${MTG_FONTS:-$B/../assets/fonts} MTG_ICONS=${MTG_ICONS:-$B/../assets/icons}
export MTG_LOGO=$B/coinzoom-disc.png MTG_URL=${MTG_URL:-mtgtribe.com}
export MTG_TRACK=${MTG_TRACK:-$B/../assets/they-call-me-mtg-closing-track.mp3}

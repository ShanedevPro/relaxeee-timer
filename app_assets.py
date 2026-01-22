from typing import Dict, List

PALETTES: Dict[str, Dict[str, str]] = {
    "Emerald": {
        "bg": "#0C0C0C",
        "panel": "#1A1A1A",
        "fg": "#33FF33",
        "accent": "#28CC28",
        "canvas": "#101810",
    },
    "Sunset": {
        "bg": "#140B0B",
        "panel": "#241212",
        "fg": "#F76C6C",
        "accent": "#E8505B",
        "canvas": "#1E0F0F",
    },
    "Ocean": {
        "bg": "#0B1116",
        "panel": "#121F2A",
        "fg": "#6ED2FF",
        "accent": "#3AAED8",
        "canvas": "#0E171E",
    },
    "Amber": {
        "bg": "#14110B",
        "panel": "#241E12",
        "fg": "#FFD166",
        "accent": "#F4A261",
        "canvas": "#1A160D",
    },
    "Slate": {
        "bg": "#0E1013",
        "panel": "#1A1D22",
        "fg": "#B6C2D9",
        "accent": "#8093B2",
        "canvas": "#12151A",
    },
}

ANIMALS: Dict[str, List[str]] = {
    "cat": [
        " /\\_/\\\n( o.o )\n /|_|\\\n  o o ",
        " /\\_/\\\n( o.o )\n /|_|\\\n o   o",
    ],
    "dog": [
        " / \\__\n(    @\\___\n /         O\n/   (_____/\n  o  o ",
        " / \\__\n(    @\\___\n /         O\n/   (_____/\n o    o",
    ],
    "fox": [
        " /\\_/\\\n( o.o )\n /|_|\\\n  v v ",
        " /\\_/\\\n( o.o )\n /|_|\\\n v   v",
    ],
    "bunny": [
        " (\\_/)\n (o o)\n /|_|\\\n  o o ",
        " (\\_/)\n (o o)\n /|_|\\\n o   o",
    ],
    "turtle": [
        "  ____\n / __ \\\n| (  ) |\n \\_~~_/\n  o  o ",
        "  ____\n / __ \\\n| (  ) |\n \\_~~_/\n o   o",
    ],
    "duck": [
        "  __\n<(o )___\n ( ._> /\n  `---'\n  o  o ",
        "  __\n<(o )___\n ( ._> /\n  `---'\n o   o",
    ],
    "owl": [
        "  ,_,\n (O,O)\n /) (\\\n  o o ",
        "  ,_,\n (O,O)\n /) (\\\n o   o",
    ],
}

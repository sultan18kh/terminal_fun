"""Animated Eid Mubarak terminal greeting.

Renders a visually stunning "Eid Mubarak" message with twinkling stars,
Islamic geometric borders, ASCII art text, and a typewriter subtitle.
"""

from __future__ import annotations

import curses
import random
import shutil
import time
from typing import Any

import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# ---------------------------------------------------------------------------
# Color themes: (primary, secondary, accent) as RGB tuples
# ---------------------------------------------------------------------------
THEMES: dict[str, dict[str, tuple[int, int, int]]] = {
    "classic": {
        "primary": (46, 204, 113),    # Green #2ecc71
        "secondary": (241, 196, 15),  # Gold #f1c40f
        "accent": (236, 240, 241),    # White #ecf0f1
    },
    "royal": {
        "primary": (108, 52, 131),    # Deep Purple #6c3483
        "secondary": (212, 172, 13),  # Gold #d4ac0d
        "accent": (253, 235, 208),    # Cream #fdebd0
    },
    "minimal": {
        "primary": (255, 255, 255),   # White #ffffff
        "secondary": (189, 195, 199), # Silver #bdc3c7
        "accent": (169, 223, 191),    # Soft Green #a9dfbf
    },
}

STAR_CHARS = ["✦", "✧", "·", "*", "⋆", "∗"]
DECORATION_CHARS = ["☪", "✦", "✧"]
MIN_COLS = 80
MIN_ROWS = 24

# ---------------------------------------------------------------------------
# Pyfiglet helpers
# ---------------------------------------------------------------------------

FONT_CHAIN = ["slant", "banner3-D", "starwars", "isometric1", "standard"]
MAX_ART_HEIGHT = 12


def get_figlet_text(text: str, max_width: int) -> list[str]:
    """Generate ASCII art text, trying fonts until one fits width and height."""
    for font in FONT_CHAIN:
        try:
            fig = pyfiglet.figlet_format(text, font=font)
            lines = [l.rstrip() for l in fig.rstrip("\n").split("\n")]
            # Strip trailing empty lines
            while lines and not lines[-1]:
                lines.pop()
            widest = max(len(line) for line in lines) if lines else 0
            if widest <= max_width - 4 and len(lines) <= MAX_ART_HEIGHT:
                return lines
        except pyfiglet.FontNotFound:
            continue
    # ultimate fallback — plain text
    return [text]


# ---------------------------------------------------------------------------
# Build the complete static frame (list of strings)
# ---------------------------------------------------------------------------

def _build_frame(cols: int) -> list[str]:
    """Compose the full greeting frame as a list of strings."""
    inner_width = cols - 2  # inside the border ║...║

    # -- ASCII art text --
    art_lines = get_figlet_text("Eid Mubarak", inner_width - 4)

    # -- decoration row --
    deco_pattern = "  ✦  ✧  ✦        ☪  ✦  ✧  ✦  ✧  ✦        ☪  ✦  ✧  ✦  "
    # tile or truncate to fit
    if len(deco_pattern) < inner_width:
        repeats = (inner_width // len(deco_pattern)) + 1
        deco_pattern = (deco_pattern * repeats)[:inner_width]
    else:
        deco_pattern = deco_pattern[:inner_width]

    subtitle = "🌙 Wishing you and your family a blessed Eid! 🌙"

    # -- assemble lines --
    frame: list[str] = []

    # top border
    frame.append("╔" + "═" * inner_width + "╗")

    # decoration row
    frame.append("║" + deco_pattern.center(inner_width) + "║")

    # blank
    frame.append("║" + " " * inner_width + "║")

    # ASCII art (centered)
    for line in art_lines:
        padded = line.center(inner_width)[:inner_width]
        frame.append("║" + padded + "║")

    # blank
    frame.append("║" + " " * inner_width + "║")

    # subtitle
    frame.append("║" + subtitle.center(inner_width) + "║")

    # blank
    frame.append("║" + " " * inner_width + "║")

    # decoration row
    frame.append("║" + deco_pattern.center(inner_width) + "║")

    # bottom border
    frame.append("╚" + "═" * inner_width + "╝")

    return frame


# ---------------------------------------------------------------------------
# Static rendering (Rich)
# ---------------------------------------------------------------------------

def _render_static(theme_name: str) -> None:
    """Render the greeting as a styled Rich panel (no animation)."""
    theme = THEMES.get(theme_name, THEMES["classic"])
    cols, _ = shutil.get_terminal_size((100, 30))
    console = Console(width=cols)

    # Use a width that fits the terminal
    frame_width = min(cols, 100)
    inner_width = frame_width - 4  # panel border padding

    art_lines = get_figlet_text("Eid Mubarak", inner_width - 2)

    deco_pattern = "✦  ✧  ✦        ☪  ✦  ✧  ✦  ✧  ✦        ☪  ✦  ✧  ✦"

    pr, pg, pb = theme["primary"]
    sr, sg, sb = theme["secondary"]
    ar, ag, ab = theme["accent"]

    body = Text(justify="center")

    # decoration row
    body.append(deco_pattern + "\n", style=f"rgb({sr},{sg},{sb})")
    body.append("\n")

    # ASCII art with gradient: line-by-line transition from primary → secondary
    # Pad all art lines to same width so centering is uniform
    art_width = max((len(line) for line in art_lines), default=0)
    total = max(len(art_lines), 1)
    for i, line in enumerate(art_lines):
        t = i / total
        r = int(pr + (sr - pr) * t)
        g = int(pg + (sg - pg) * t)
        b = int(pb + (sb - pb) * t)
        body.append(line.ljust(art_width) + "\n", style=f"bold rgb({r},{g},{b})")

    body.append("\n")

    # subtitle
    subtitle = "🌙 Wishing you and your family a blessed Eid! 🌙"
    body.append(subtitle + "\n", style=f"rgb({ar},{ag},{ab})")
    body.append("\n")

    # decoration row
    body.append(deco_pattern, style=f"rgb({sr},{sg},{sb})")

    panel = Panel(
        body,
        border_style=f"rgb({sr},{sg},{sb})",
        title="[bold]☪ Eid Mubarak ☪[/bold]",
        title_align="center",
        width=frame_width,
    )
    console.print(panel, justify="center")


# ---------------------------------------------------------------------------
# Curses helpers
# ---------------------------------------------------------------------------

def _rgb_to_curses_color(r: int, g: int, b: int) -> tuple[int, int, int]:
    """Convert 0-255 RGB to curses 0-1000 range."""
    return (r * 1000 // 255, g * 1000 // 255, b * 1000 // 255)


def _init_colors(theme: dict[str, tuple[int, int, int]]) -> dict[str, int]:
    """Initialize curses color pairs; returns mapping name → pair number.

    Falls back to default colors if the terminal doesn't support color changes.
    """
    pairs: dict[str, int] = {}

    can_change = curses.can_change_color()

    if can_change:
        # Define custom colors starting at index 16 to avoid clobbering defaults
        color_defs = {
            "primary": (16, theme["primary"]),
            "secondary": (17, theme["secondary"]),
            "accent": (18, theme["accent"]),
            "star": (19, (200, 200, 200)),
            "star_dim": (20, (100, 100, 100)),
        }
        for _, (idx, rgb) in color_defs.items():
            cr, cg, cb = _rgb_to_curses_color(*rgb)
            try:
                curses.init_color(idx, cr, cg, cb)
            except curses.error:
                can_change = False
                break

    if can_change:
        curses.init_pair(1, 16, curses.COLOR_BLACK)  # primary
        curses.init_pair(2, 17, curses.COLOR_BLACK)   # secondary
        curses.init_pair(3, 18, curses.COLOR_BLACK)   # accent
        curses.init_pair(4, 19, curses.COLOR_BLACK)   # star bright
        curses.init_pair(5, 20, curses.COLOR_BLACK)   # star dim
    else:
        # Fallback: use standard colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    pairs["primary"] = curses.color_pair(1)
    pairs["secondary"] = curses.color_pair(2)
    pairs["accent"] = curses.color_pair(3)
    pairs["star"] = curses.color_pair(4)
    pairs["star_dim"] = curses.color_pair(5)

    return pairs


def _safe_addstr(stdscr: Any, y: int, x: int, text: str, attr: int = 0) -> None:
    """Write string to curses window, silently ignoring out-of-bounds writes."""
    max_y, max_x = stdscr.getmaxyx()
    if y < 0 or y >= max_y or x < 0:
        return
    # Truncate text to fit within the screen width
    available = max_x - x
    if available <= 0:
        return
    truncated = text[:available]
    try:
        stdscr.addstr(y, x, truncated, attr)
    except curses.error:
        # addstr raises error when writing to bottom-right corner; ignore it
        pass


# ---------------------------------------------------------------------------
# Animated rendering (curses)
# ---------------------------------------------------------------------------

def _generate_stars(rows: int, cols: int, count: int) -> list[tuple[int, int]]:
    """Generate random star positions."""
    stars = []
    for _ in range(count):
        y = random.randint(0, rows - 1)
        x = random.randint(0, cols - 1)
        stars.append((y, x))
    return stars


def _animate(stdscr: Any, theme_name: str) -> None:
    """Run the full animation sequence inside curses."""
    curses.curs_set(0)  # hide cursor
    stdscr.nodelay(True)  # non-blocking getch
    stdscr.clear()

    rows, cols = stdscr.getmaxyx()

    # Check minimum size
    if cols < MIN_COLS or rows < MIN_ROWS:
        stdscr.nodelay(False)
        msg = f"Terminal too small ({cols}x{rows}). Need at least {MIN_COLS}x{MIN_ROWS}."
        _safe_addstr(stdscr, rows // 2, max(0, (cols - len(msg)) // 2), msg)
        stdscr.refresh()
        stdscr.getch()
        return

    theme = THEMES.get(theme_name, THEMES["classic"])
    colors = _init_colors(theme)

    # -- Prepare content --
    inner_width = min(cols - 2, 98)  # border content width
    art_lines = get_figlet_text("Eid Mubarak", inner_width - 4)

    deco_pattern = "  ✦  ✧  ✦        ☪  ✦  ✧  ✦  ✧  ✦        ☪  ✦  ✧  ✦  "
    if len(deco_pattern) < inner_width:
        repeats = (inner_width // len(deco_pattern)) + 1
        deco_pattern = (deco_pattern * repeats)[:inner_width]
    else:
        deco_pattern = deco_pattern[:inner_width]

    subtitle = "🌙 Wishing you and your family a blessed Eid! 🌙"

    # Build the frame content (without the outer ║ border chars)
    frame_content: list[str] = []
    frame_content.append("═" * inner_width)  # top border fill
    frame_content.append(deco_pattern.center(inner_width))
    frame_content.append(" " * inner_width)
    for line in art_lines:
        frame_content.append(line.center(inner_width)[:inner_width])
    frame_content.append(" " * inner_width)
    frame_content.append(subtitle.center(inner_width)[:inner_width])
    frame_content.append(" " * inner_width)
    frame_content.append(deco_pattern.center(inner_width))
    frame_content.append("═" * inner_width)  # bottom border fill

    frame_height = len(frame_content)
    start_y = max(0, (rows - frame_height) // 2)
    start_x = max(0, (cols - inner_width - 2) // 2)

    # Star positions (outside the main frame area)
    num_stars = min(60, (rows * cols) // 50)
    stars = _generate_stars(rows, cols, num_stars)

    # -----------------------------------------------------------------------
    # Phase 1: Twinkling stars (30 frames)
    # -----------------------------------------------------------------------
    for _ in range(30):
        stdscr.erase()
        for sy, sx in stars:
            brightness = random.random()
            char = random.choice(STAR_CHARS)
            attr = colors["star"] if brightness > 0.4 else colors["star_dim"]
            _safe_addstr(stdscr, sy, sx, char, attr)
        stdscr.refresh()
        time.sleep(0.05)
        if stdscr.getch() != -1:
            return

    # -----------------------------------------------------------------------
    # Phase 2: Draw border (animated)
    # -----------------------------------------------------------------------
    # Top border
    _safe_addstr(stdscr, start_y, start_x, "╔", colors["secondary"] | curses.A_BOLD)
    for i in range(inner_width):
        # keep stars twinkling
        for sy, sx in random.sample(stars, min(10, len(stars))):
            char = random.choice(STAR_CHARS)
            attr = colors["star"] if random.random() > 0.4 else colors["star_dim"]
            _safe_addstr(stdscr, sy, sx, char, attr)

        _safe_addstr(stdscr, start_y, start_x + 1 + i, "═", colors["secondary"])
        if i % 4 == 0:
            stdscr.refresh()
            time.sleep(0.01)
        if stdscr.getch() != -1:
            return
    _safe_addstr(stdscr, start_y, start_x + inner_width + 1, "╗", colors["secondary"] | curses.A_BOLD)
    stdscr.refresh()

    # Side borders
    for row_i in range(1, frame_height - 1):
        y = start_y + row_i
        _safe_addstr(stdscr, y, start_x, "║", colors["secondary"])
        _safe_addstr(stdscr, y, start_x + inner_width + 1, "║", colors["secondary"])
    stdscr.refresh()
    time.sleep(0.1)

    # Bottom border
    _safe_addstr(stdscr, start_y + frame_height - 1, start_x, "╚", colors["secondary"] | curses.A_BOLD)
    for i in range(inner_width):
        _safe_addstr(stdscr, start_y + frame_height - 1, start_x + 1 + i, "═", colors["secondary"])
        if i % 4 == 0:
            stdscr.refresh()
            time.sleep(0.01)
        if stdscr.getch() != -1:
            return
    _safe_addstr(stdscr, start_y + frame_height - 1, start_x + inner_width + 1, "╝",
                 colors["secondary"] | curses.A_BOLD)
    stdscr.refresh()
    time.sleep(0.2)

    # -----------------------------------------------------------------------
    # Phase 3: Decoration rows (instant)
    # -----------------------------------------------------------------------
    # Top deco row
    deco_y_top = start_y + 1
    deco_text = frame_content[1]
    _safe_addstr(stdscr, deco_y_top, start_x + 1, deco_text, colors["secondary"])
    stdscr.refresh()
    time.sleep(0.3)

    # -----------------------------------------------------------------------
    # Phase 4: Reveal ASCII art character by character
    # -----------------------------------------------------------------------
    art_start_idx = 3  # index in frame_content where art lines begin
    total_art = len(art_lines)
    for li, line in enumerate(art_lines):
        y = start_y + art_start_idx + li
        centered = line.center(inner_width)[:inner_width]
        # Gradient: interpolate from primary to secondary across lines
        t = li / max(total_art - 1, 1)
        if t < 0.5:
            attr = colors["primary"] | curses.A_BOLD
        else:
            attr = colors["secondary"] | curses.A_BOLD

        # Reveal character by character
        for ci, ch in enumerate(centered):
            if ch != " ":
                _safe_addstr(stdscr, y, start_x + 1 + ci, ch, attr)

                # twinkle some stars each char
                if ci % 3 == 0:
                    for sy, sx in random.sample(stars, min(5, len(stars))):
                        char = random.choice(STAR_CHARS)
                        star_attr = colors["star"] if random.random() > 0.4 else colors["star_dim"]
                        _safe_addstr(stdscr, sy, sx, char, star_attr)

        stdscr.refresh()
        time.sleep(0.08)
        if stdscr.getch() != -1:
            return

    time.sleep(0.3)

    # -----------------------------------------------------------------------
    # Phase 5: Fade in crescent moon & star decorations
    # -----------------------------------------------------------------------
    # Place ☪ decorations at corners of the art area
    moon_positions = [
        (start_y + 2, start_x + 3),
        (start_y + 2, start_x + inner_width - 2),
        (start_y + frame_height - 3, start_x + 3),
        (start_y + frame_height - 3, start_x + inner_width - 2),
    ]
    for my, mx in moon_positions:
        _safe_addstr(stdscr, my, mx, "☪", colors["secondary"] | curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.15)
        if stdscr.getch() != -1:
            return

    time.sleep(0.2)

    # -----------------------------------------------------------------------
    # Phase 6: Typewriter subtitle
    # -----------------------------------------------------------------------
    sub_idx = art_start_idx + total_art + 1  # +1 for blank line after art
    sub_y = start_y + sub_idx
    sub_centered = subtitle.center(inner_width)[:inner_width]
    for ci, ch in enumerate(sub_centered):
        if ch != " ":
            _safe_addstr(stdscr, sub_y, start_x + 1 + ci, ch, colors["accent"] | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.03)
            if stdscr.getch() != -1:
                return
        elif ci > 0 and sub_centered[ci - 1] != " ":
            # small pause at word boundaries
            stdscr.refresh()

    stdscr.refresh()
    time.sleep(0.3)

    # Bottom deco row
    deco_y_bot = start_y + frame_height - 2
    _safe_addstr(stdscr, deco_y_bot, start_x + 1, frame_content[-2], colors["secondary"])
    stdscr.refresh()

    # -----------------------------------------------------------------------
    # Phase 7: Hold — keep twinkling until keypress
    # -----------------------------------------------------------------------
    stdscr.nodelay(True)
    while True:
        # Twinkle stars
        for sy, sx in stars:
            char = random.choice(STAR_CHARS)
            attr = colors["star"] if random.random() > 0.4 else colors["star_dim"]
            _safe_addstr(stdscr, sy, sx, char, attr)
        stdscr.refresh()
        time.sleep(0.1)
        if stdscr.getch() != -1:
            return


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run(static: bool = False, theme: str = "classic") -> None:
    """Run the Eid Mubarak greeting tool."""
    if theme not in THEMES:
        valid = ", ".join(THEMES.keys())
        print(f"Unknown theme '{theme}'. Valid themes: {valid}")
        raise SystemExit(1)

    if static:
        _render_static(theme)
    else:
        curses.wrapper(lambda stdscr: _animate(stdscr, theme))

# terminal_fun

🎨 A collection of fun, visually striking terminal-based tools and animations. From festive greetings (Eid Mubarak, Ramadan Kareem) to creative ASCII art and CLI eye-candy — built to impress in screenshots and LinkedIn posts. Powered by Python with Rich, Curses & more. Contributions welcome! #TerminalArt #CLI #Python

---

## 🚀 Quick Start

```bash
# Clone the repository`
git clone https://github.com/sultankh18/terminal_fun.git
cd terminal_fun

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run a tool
python -m terminal_fun eid-mubarak
```

---

## 📁 Project Structure

```
terminal_fun/
├── terminal_fun/
│   ├── __init__.py
│   ├── __main__.py          # CLI entry point (Typer app)
│   └── tools/
│       ├── __init__.py
│       └── eid_mubarak.py   # 🌙 Animated Eid Mubarak greeting
├── assets/
│   └── screenshots/         # Terminal screenshots for LinkedIn / README
├── tests/
│   └── test_eid_mubarak.py
├── requirements.txt
├── pyproject.toml
├── CLAUDE.md                # Claude Code project context
├── LICENSE                  # MIT License
└── README.md
```

---

## 🌙 Tool #1: Eid Mubarak — Animated Terminal Greeting

An animated, colorful "Eid Mubarak" message rendered directly in the terminal — designed to look stunning in screenshots and LinkedIn posts.

### Features

- Large ASCII art text banner using **Pyfiglet** (font: `starwars`, `banner3-D`, or `isometric1`)
- Animated entrance effect: characters revealed progressively with a typing/fade-in animation
- Crescent moon & star ASCII art border decoration
- Color gradient transition (green → gold → white) using **Rich** library
- Twinkling star particles in the background using **Curses**
- Decorative Islamic geometric pattern border (box-drawing characters)
- Subtitle line: *"Wishing you and your family a blessed Eid!"* with a typewriter effect
- Auto-sized to terminal width for clean screenshots at any resolution
- Optional `--static` flag to skip animation and print the final frame (for quick screenshots)
- Optional `--theme` flag to switch color palettes (`classic`, `royal`, `minimal`)

### Usage

```bash
# Default animated version
python -m terminal_fun eid-mubarak

# Static mode (no animation, instant render — ideal for screenshots)
python -m terminal_fun eid-mubarak --static

# Choose a color theme
python -m terminal_fun eid-mubarak --theme royal

# Save output to a text file (static mode auto-enabled)
python -m terminal_fun eid-mubarak --static > eid_output.txt
```

### Implementation Details

**Stack:**

| Component | Library | Purpose |
|-----------|---------|---------|
| ASCII Art Text | `pyfiglet` | Large banner text generation ("Eid Mubarak") |
| Colors & Panels | `rich` | RGB color gradients, styled panels, console output |
| Full-screen Animation | `curses` | Background star particles, frame-by-frame rendering |
| CLI Interface | `typer` | Command-line argument parsing, subcommands |
| Terminal Size Detection | `shutil.get_terminal_size()` | Responsive layout |

**Animation Pipeline:**

1. Clear screen and initialize curses window
2. Render twinkling star particles across the background (random positions, brightness cycle)
3. Draw Islamic geometric border using box-drawing Unicode characters (`╔`, `═`, `╗`, `║`, `╚`, `╝`, `✦`, `✧`)
4. Reveal ASCII art "Eid Mubarak" text character-by-character with color gradient
5. Fade in crescent moon (`☪`) and star decorations
6. Typewriter-animate the subtitle message
7. Hold final frame until user presses any key

**Color Themes:**

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| `classic` | Green `#2ecc71` | Gold `#f1c40f` | White `#ecf0f1` |
| `royal` | Deep Purple `#6c3483` | Gold `#d4ac0d` | Cream `#fdebd0` |
| `minimal` | White `#ffffff` | Silver `#bdc3c7` | Soft Green `#a9dfbf` |

### Example Output (Static)

```
╔══════════════════════════════════════════════════════════════╗
║  ✦  ✧  ✦        ☪  ✦  ✧  ✦  ✧  ✦        ☪  ✦  ✧  ✦      ║
║                                                              ║
║     _____ _     _   __  __       _                _          ║
║    | ____(_) __| | |  \/  |_   _| |__   __ _ _ __| | __     ║
║    |  _| | |/ _` | | |\/| | | | | '_ \ / _` | '__| |/ /    ║
║    | |___| | (_| | | |  | | |_| | |_) | (_| | |  |   <     ║
║    |_____|_|\__,_| |_|  |_|\__,_|_.__/ \__,_|_|  |_|\_\    ║
║                                                              ║
║          🌙 Wishing you and your family a blessed Eid! 🌙    ║
║                                                              ║
║  ✦  ✧  ✦        ☪  ✦  ✧  ✦  ✧  ✦        ☪  ✦  ✧  ✦      ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 🛠 Tech Stack

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Core language |
| [Rich](https://github.com/Textualize/rich) | 13.x | Terminal colors, styling, panels |
| [Pyfiglet](https://github.com/pwaller/pyfiglet) | 1.0+ | ASCII art text |
| [Typer](https://github.com/tiangolo/typer) | 0.9+ | CLI framework |
| curses | stdlib | Full-screen terminal animations |

### `requirements.txt`

```
rich>=13.0.0
pyfiglet>=1.0.0
typer>=0.9.0
```

---

## 🗺 Roadmap

- [x] Eid Mubarak animated greeting
- [ ] Ramadan Kareem countdown timer
- [ ] ASCII art clock (live updating)
- [ ] Terminal-based Quran verse of the day
- [ ] Pakistan Independence Day (14 Aug) animation
- [ ] Generic birthday greeting generator
- [ ] Matrix-style rain effect with custom text
- [ ] `--record` flag to export animation as GIF (using `termtosvg` or `asciinema`)

---

## 📸 Screenshots for LinkedIn

For the best LinkedIn screenshots:

1. Use a dark terminal theme (e.g., Dracula, One Dark, or plain black)
2. Set font size to 14–16pt for readability
3. Run with `--static` flag for a clean single frame
4. Use a terminal with ligature support (e.g., Windows Terminal, iTerm2, Kitty)
5. Capture at 1200×630px for LinkedIn's recommended image ratio
6. Consider using `termtosvg` or `asciinema` for animated recordings

---

## 🤝 Contributing

Contributions are welcome! To add a new terminal tool:

1. Create a new file in `terminal_fun/tools/` (e.g., `my_tool.py`)
2. Implement a `run()` function as the entry point
3. Register the subcommand in `terminal_fun/__main__.py`
4. Add documentation to this README under a new `## Tool #N` section
5. Submit a PR!

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Sultan Khan** — Senior Solution Developer II @ AlphaBOLD, Lahore, Pakistan

- GitHub: [@sultankh18](https://github.com/sultankh18)
- LinkedIn: [Sultan Khan](https://linkedin.com/in/sultankh18)

---

> *Built with ❤️ and a love for beautiful terminals.*
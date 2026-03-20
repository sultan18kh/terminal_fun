# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**terminal_fun** is a collection of visually striking terminal-based tools and animations (Eid Mubarak greeting, Ramadan countdown, ASCII art, etc.) built in Python 3.10+.

## Commands

```bash
# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run a tool
python -m terminal_fun eid-mubarak
python -m terminal_fun eid-mubarak --static        # no animation
python -m terminal_fun eid-mubarak --theme royal    # color theme

# Run tests
pip install pytest
python -m pytest tests/ -v

# Run a single test
python -m pytest tests/test_eid_mubarak.py::TestStaticMode -v
```

## Architecture

- **CLI layer:** Typer app in `terminal_fun/__main__.py` — each tool is a subcommand
- **Tools:** Each tool lives in `terminal_fun/tools/<tool_name>.py` with a `run()` entry point
- **Rendering stack:** curses (full-screen animation), Rich (styled output/gradients), Pyfiglet (ASCII art banners)
- **Adding a new tool:** create module in `tools/` with a `run()` function, then register it as a `typer.Typer` sub-app via `app.add_typer()` in `__main__.py`
- **Dual rendering:** each tool uses curses for animated mode and Rich for `--static` mode

## Dependencies

- **rich** >=13.0.0 — terminal colors, panels, gradients
- **pyfiglet** >=1.0.0 — ASCII art text generation
- **typer** >=0.9.0 — CLI framework
- **curses** (stdlib) — full-screen terminal animations

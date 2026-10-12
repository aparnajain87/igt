# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

Python 3.11 is required (3.9 lacks binary wheels for `tables`, causing build failures). A `.venv311` virtual environment is already set up:

```bash
source .venv311/bin/activate
python main.py
```

To recreate from scratch:
```bash
uv venv --python 3.11 .venv311
uv pip install psychopy --python .venv311/bin/python
```

## Linting

```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Architecture

**`main.py`** — Entry point. Creates the PsychoPy `Window`, all `TextStim`/`ShapeStim` UI objects, and runs the main game loop using `psychopy.event.waitKeys()` for blocking keyboard input. Calls `drawMainUI()` to redraw the header/stats panel, then highlights the chosen deck letter green after each keypress. Keys: `a`, `b`, `c`, `d` to select a deck; `q` to quit.

**`participant.py`** — `Participant` base class (name, instance counter) and `trialParticipant` subclass. `trialParticipant` tracks running `__winnings` (int) and `__charsPressed` dict (`{a,b,c,d: count}`). `setWinnings(winnings_loses)` takes a `(won, lost)` tuple and updates the total.

**`filemanager.py`** — `FileManager` base class (generic CSV reader: `readRow(r)`, `getTotalRows()`). `DeckFileManager` subclass hardcodes `Decks.csv` as the source. Four instances are created in `main.py`; each gets a `decknumber` (1–4) via a class-level `instanceCount`. `getWinsLoses()` slices the correct column pair from the CSV row based on `decknumber` and advances `rowNumber`.

**`Decks.csv`** — 16 data rows (row 0 is header). Column layout: `DeckA_Won, DeckA_Lost, DeckB_Won, DeckB_Lost, DeckC_Won, DeckC_Lost, DeckD_Won, DeckD_Lost`. `DeckFileManager` reads columns `[0:2]`, `[2:4]`, `[4:6]`, `[6:8]` for decks A–D respectively.

# Iowa Gambling Task Implementation

The Iowa Gambling Task is a psychological task designed to simulate real-life decision making. Participants repeatedly choose from four decks of cards to maximise their winnings, and the task measures their ability to learn advantageous long-term strategies over short-term gains.

![Iowa Gambling Task Mockup](https://cs1.ucc.ie/~jl22/iowaGamblingTaskMockup_JL_117372043.png "Iowa Gambling Task Implementation - Jack Leonard - 117372043")

## How It Works

### The Decks

There are four decks — A, B, C, and D. Each deck has a different win/loss profile defined in `Decks.csv`:

| Deck | Wins | Losses | Net Tendency |
|------|------|--------|--------------|
| A | High | High | Net negative |
| B | High | High | Net negative |
| C | Low  | Low  | Net positive |
| D | Low  | Low  | Net positive |

Decks A and B offer tempting high rewards but come with large losses that outweigh the gains over time. Decks C and D offer modest rewards with smaller losses, making them the advantageous long-term choices. The task measures whether participants learn to favour C and D.

### Gameplay

1. A PsychoPy window opens showing the participant's current winnings and four deck labels (A, B, C, D).
2. The participant presses a key (`a`, `b`, `c`, or `d`) to select a deck.
3. The selected deck highlights green, and the win/loss amounts for that draw are displayed.
4. The participant's running total is updated and shown on screen.
5. This repeats for up to 16 rounds (the number of rows in `Decks.csv`).
6. When all rows are exhausted or the participant presses `q`, the game ends and a summary screen displays the final winnings for 10 seconds.

### Data Flow

- `Decks.csv` holds all win/loss values. Each row is one round; each deck occupies two columns (amount won, amount lost).
- `DeckFileManager` (in `filemanager.py`) reads the appropriate column pair for its deck on each keypress and advances its internal row counter.
- `trialParticipant` (in `participant.py`) accumulates the running winnings total and records how many times each deck was selected.

## Setup

Python 3.11 and `uv` are required.

```bash
uv venv --python 3.11 .venv311
uv pip install psychopy --python .venv311/bin/python
```

## Running

```bash
.venv311/bin/python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `a` | Draw from Deck A |
| `b` | Draw from Deck B |
| `c` | Draw from Deck C |
| `d` | Draw from Deck D |
| `q` | Quit |

## Project Structure

```
main.py          # PsychoPy UI and main game loop
participant.py   # Participant class — tracks winnings and key presses
filemanager.py   # CSV reader and per-deck data access
Decks.csv        # Win/loss values for all four decks (16 rounds)
older/           # Archived earlier versions
```

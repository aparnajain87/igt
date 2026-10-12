'''

################## MAIN.PY ########################
                © Jack Leonard 2019
      117372043 - Iowa Gambling Task Project

            Main Code & Psychopy based GUI

###################################################
'''

#       ↓ Document Imports
from participant import Participant, trialParticipant
from filemanager import FileManager, DeckFileManager

#       ↓  Psychopy/External Dependency Imports
from psychopy.visual import Window, TextStim, ShapeStim
import psychopy.visual
from psychopy import event, core, monitors

#       -> Instantiating Classes
participantA = trialParticipant()
deckA = DeckFileManager()
deckB = DeckFileManager()
deckC = DeckFileManager()
deckD = DeckFileManager()

#       ↓ Monitor Topology Setup
mon = monitors.Monitor('testMonitor')
mon.setSizePix([1080, 810])
mon.setWidth(53)
mon.setDistance(57)

display = Window(
    size=(1080, 810),
    monitor=mon,
    units="pix",
    color="#FFFFFF",
    fullscr=False,
    allowGUI=True,
    useRetina=True,
)

# ===== CONSTANTS =====
BAR_LEFT  = -330    # x of bar left edge (pixels)
BAR_WIDTH = 660     # total bar width (pixels, represents $0–$8000)
BAR_MAX   = 8000    # scale maximum

CARD_Y       = -155
CARD_W       = 130
CARD_H       = 185
CARD_BLUE    = "#1a3a8a"
CARD_POSITIONS = {'a': -300, 'b': -100, 'c': 100, 'd': 300}

totalRounds = deckA.getTotalRows() - 1   # 16
round_count = 0

# ===== WINNINGS BAR SECTION =====

winningsTitleText = TextStim(
    win=display, pos=(0, 375),
    text="Winnings:", font='Arial', bold=True, alignText='center',
    color="#000000", height=40,
)

# Scale markers 0 – 8000
scaleMarkers = []
for val in range(0, BAR_MAX + 1, 1000):
    x = BAR_LEFT + (val / BAR_MAX) * BAR_WIDTH
    scaleMarkers.append(TextStim(
        win=display, pos=(x, 340),
        text=str(val), font='Arial', alignText='center',
        color="#555555", height=14,
    ))

# Green earnings bar
winningsBarTrack = psychopy.visual.Rect(
    win=display, pos=(BAR_LEFT + BAR_WIDTH / 2, 315),
    size=(BAR_WIDTH, 22),
    fillColor="#DDDDDD", lineColor="#AAAAAA", lineWidth=1, units="pix"
)
winningsBarFill = psychopy.visual.Rect(
    win=display, pos=(BAR_LEFT + 0.5, 315),
    size=(1, 22),
    fillColor="#2E7D32", lineColor=None, units="pix"
)

# Earnings label (left of green bar) and live $ value (right of bar)
barEarningsLabel = TextStim(
    win=display, pos=(-430, 315),
    text="Earnings", font='Arial', alignText='right',
    color="#2E7D32", height=16,
)
earningsValueText = TextStim(
    win=display, pos=(BAR_LEFT + BAR_WIDTH + 18, 315),
    text="$0", font='Arial', bold=True, alignText='left',
    color="#2E7D32", height=18,
)

# Section dividers
divider1 = psychopy.visual.Rect(
    win=display, pos=(0, 252), size=(780, 1),
    fillColor="#CCCCCC", lineColor=None, units="pix"
)
divider2 = psychopy.visual.Rect(
    win=display, pos=(0, 52), size=(780, 1),
    fillColor="#CCCCCC", lineColor=None, units="pix"
)

# ===== WIN / LOSS FEEDBACK =====

resultHeaderText = TextStim(
    win=display, pos=(0, 225),
    text="", font='Arial', bold=True, alignText='center',
    color="#888888", height=18,
)
feedbackBgRect = psychopy.visual.Rect(
    win=display, pos=(0, 148),
    size=(500, 85),
    fillColor="#EEEEEE", lineColor="#CCCCCC", lineWidth=1, units="pix"
)
feedbackText = TextStim(
    win=display, pos=(0, 148),
    text="Select a deck to begin", font='Arial', bold=True, alignText='center',
    color="#888888", height=30,
)
resultDetailText = TextStim(
    win=display, pos=(0, 88),
    text="", font='Arial', alignText='center',
    color="#555555", height=18,
)

# Waiting prompt shown while game awaits key input
waitingText = TextStim(
    win=display, pos=(0, -308),
    text="Press  A  B  C  or  D  to select a deck",
    font='Arial', alignText='center',
    color="#888888", height=20,
)

# ===== DECK CARDS =====

deckTitleTexts = {
    'a': TextStim(win=display, pos=(-300, -30), text="A", font='Arial', bold=True, alignText='center', color="#000000", height=22),
    'b': TextStim(win=display, pos=(-100, -30), text="B", font='Arial', bold=True, alignText='center', color="#000000", height=22),
    'c': TextStim(win=display, pos=( 100, -30), text="C", font='Arial', bold=True, alignText='center', color="#000000", height=22),
    'd': TextStim(win=display, pos=( 300, -30), text="D", font='Arial', bold=True, alignText='center', color="#000000", height=22),
}

# Legacy references used on game-over screen
deckATitleText = deckTitleTexts['a']
deckDTitleText = deckTitleTexts['d']

def makeCardParts(x, y):
    """Five nested Rects forming a playing-card-back design with drop shadow."""
    return [
        psychopy.visual.Rect(win=display, pos=(x+6, y-6), size=(CARD_W,    CARD_H   ), fillColor="#BBBBBB",  lineColor=None,      units="pix"),
        psychopy.visual.Rect(win=display, pos=(x, y),     size=(CARD_W,    CARD_H   ), fillColor="#FFFFFF",  lineColor="#AAAAAA", lineWidth=1, units="pix"),
        psychopy.visual.Rect(win=display, pos=(x, y),     size=(CARD_W-8,  CARD_H-8 ), fillColor=CARD_BLUE,  lineColor=None,      units="pix"),
        psychopy.visual.Rect(win=display, pos=(x, y),     size=(CARD_W-24, CARD_H-24), fillColor="#FFFFFF",  lineColor=None,      units="pix"),
        psychopy.visual.Rect(win=display, pos=(x, y),     size=(CARD_W-30, CARD_H-30), fillColor=CARD_BLUE,  lineColor=None,      units="pix"),
    ]

cardParts = {k: makeCardParts(CARD_POSITIONS[k], CARD_Y) for k in CARD_POSITIONS}

# Pre-made selected-card rects (repositioned at draw time)
selectedCardShadow = psychopy.visual.Rect(
    win=display, pos=(6, CARD_Y - 6),
    size=(CARD_W, CARD_H),
    fillColor="#BBBBBB", lineColor=None, units="pix"
)
selectedCardRect = psychopy.visual.Rect(
    win=display, pos=(0, CARD_Y),
    size=(CARD_W, CARD_H),
    fillColor="#C62828", lineColor="#AAAAAA", lineWidth=1, units="pix"
)

# ===== ROUND COUNTER =====

roundCounterText = TextStim(
    win=display, pos=(0, -365),
    text=f"Round 0 of {totalRounds}",
    font='Arial', alignText='center',
    color="#000000", height=18,
)

# ===== INSTRUCTION SCREEN =====

instructionTitleText = TextStim(
    win=display, pos=(0, 250),
    text="Iowa Gambling Task", font='Arial', bold=True, alignText='center',
    color="#1a3a8a", height=56,
)
instructionBodyText = TextStim(
    win=display, pos=(0, 20),
    text=(
        "You will be presented with four decks of cards: A, B, C and D.\n\n"
        "On each turn, press the corresponding key to select a deck.\n\n"
        "Each draw results in a win or a loss.\n\n"
        "Some decks are more advantageous than others.\n\n"
        "Try to maximise your winnings over 16 rounds."
    ),
    font='Arial', alignText='center', color="#333333", height=24, wrapWidth=750,
)
proceedText = TextStim(
    win=display, pos=(0, -270),
    text="[ PRESS SPACE TO START ]", font='Arial', bold=True, alignText='center',
    color="#1a3a8a", height=28,
)

# ===== HELPER FUNCTIONS =====

def updateWinningsBar():
    winnings = participantA.getWinnings()
    w = max(0, min((winnings / BAR_MAX) * BAR_WIDTH, BAR_WIDTH))
    if w < 1:
        winningsBarFill.size = [1, 22]
        winningsBarFill.pos  = [BAR_LEFT + 0.5, 315]
    else:
        winningsBarFill.size = [w, 22]
        winningsBarFill.pos  = [BAR_LEFT + w / 2, 315]
    earningsValueText.text = f"${winnings}"

def drawMainUI(selectedDeck=None):
    # Bar section
    winningsTitleText.draw()
    for m in scaleMarkers:
        m.draw()
    winningsBarTrack.draw()
    winningsBarFill.draw()
    barEarningsLabel.draw()
    earningsValueText.draw()

    # Divider between bars and feedback
    divider1.draw()

    # Feedback section
    resultHeaderText.draw()
    feedbackBgRect.draw()
    feedbackText.draw()
    resultDetailText.draw()

    # Divider between feedback and cards
    divider2.draw()

    # Deck cards
    for k, parts in cardParts.items():
        if k == selectedDeck:
            selectedCardShadow.pos = (CARD_POSITIONS[k] + 6, CARD_Y - 6)
            selectedCardShadow.draw()
            selectedCardRect.pos = (CARD_POSITIONS[k], CARD_Y)
            selectedCardRect.draw()
        else:
            for part in parts:
                part.draw()

    # Deck labels
    for txt in deckTitleTexts.values():
        txt.draw()

    # Waiting prompt and round counter
    waitingText.draw()
    roundCounterText.draw()

    display.flip()


def handleDeckSelection(deckManager, deckKey):
    """Process a deck selection: update data, feedback, and redraw."""
    global round_count

    winningsLoses = deckManager.getWinsLoses()
    participantA.setWinnings(winningsLoses)
    participantA.recordKeysPressed(deckKey)

    round_count += 1
    roundCounterText.text = f"Round {round_count} of {totalRounds}"

    net = int(winningsLoses[0]) - int(winningsLoses[1])
    if net >= 0:
        feedbackBgRect.fillColor = "#2E7D32"
        feedbackText.text  = f"+${net}   You won!"
        feedbackText.color = "#FFFFFF"
    else:
        feedbackBgRect.fillColor = "#C62828"
        feedbackText.text  = f"-${abs(net)}   You lost!"
        feedbackText.color = "#FFFFFF"

    resultHeaderText.text = "Last Result:"
    resultDetailText.text = f"Won: ${winningsLoses[0]}   |   Lost: ${winningsLoses[1]}"

    updateWinningsBar()
    drawMainUI(selectedDeck=deckKey)


# ===== INSTRUCTION SCREEN =====
instructionTitleText.draw()
instructionBodyText.draw()
proceedText.draw()
display.flip()
event.waitKeys(keyList=['space'])

# ===== SHOW GAME SCREEN =====
updateWinningsBar()
drawMainUI()


# ===== MAIN GAME LOOP =====
while True:

    if round_count >= totalRounds:
        print("You have completed the game!")
        break

    char_pressed = psychopy.event.waitKeys()

    if char_pressed == ['q']:
        display.close()
        core.quit()
    elif char_pressed == ['a']:
        handleDeckSelection(deckA, 'a')
    elif char_pressed == ['b']:
        handleDeckSelection(deckB, 'b')
    elif char_pressed == ['c']:
        handleDeckSelection(deckC, 'c')
    elif char_pressed == ['d']:
        handleDeckSelection(deckD, 'd')


# ===== GAME OVER SCREEN =====
core.wait(1)

goTitle   = TextStim(win=display, pos=(0,  130), text="Trial Over",
                     font='Arial', bold=True, color="#1a3a8a", height=40, alignText='center')
goWinText = TextStim(win=display, pos=(0,   50), text=f"Final Winnings: ${participantA.getWinnings()}",
                     font='Arial', bold=True, color="#2E7D32", height=28, alignText='center')
goThanks  = TextStim(win=display, pos=(0,  -30), text="Thanks for Participating",
                     font='Arial', color="#333333", height=22, alignText='center')

# Close button
closeBtnRect = psychopy.visual.Rect(
    win=display, pos=(0, -130), size=(160, 46),
    fillColor="#1a3a8a", lineColor=None, units="pix"
)
closeBtnText = TextStim(
    win=display, pos=(0, -130), text="Close",
    font='Arial', bold=True, alignText='center', color="#FFFFFF", height=20,
)

def drawGameOver():
    display.clearBuffer()
    goTitle.draw()
    goWinText.draw()
    goThanks.draw()
    closeBtnRect.draw()
    closeBtnText.draw()
    display.flip()

drawGameOver()

mouse = event.Mouse(win=display)
mouse.clickReset()

while True:
    drawGameOver()
    # Close on button click
    if mouse.isPressedIn(closeBtnRect):
        break
    # Also allow keyboard close
    keys = event.getKeys(keyList=['q', 'escape', 'space'])
    if keys:
        break

display.close()

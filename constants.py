import math

# The proportion of the non-menu part of the application GUI that the game
# takes up
GAME_WINDOW_PROPORTION = 0.8

# The proportion that the menu takes up from the application GUI
MENU_PROPORTION = 0.1

FONT = ('Courier', 12)

# The spacing between squares in the GUI
SPACING = 5

# Spacing between colors when a square has multiple colors
INNER_SPACING = 10

# Max colors to show in a sqare
MAX_COLORS = 4

# How fast swapping takes place
SWAP_SPEED = 5

ROTATION_SPEED = math.pi / 12
SHRINK_FACTOR = 0.97
REMOVE_TIME = 75

# Image file (has to be .gif) displayed in victory splash screen

VICTORY_IMAGE = 'trophy.gif'

# How fast the vicotry image appears
IMAGE_GROWTH_FACTOR = 5, 4

# How fast to animate text
TEXT_SPEED = 20
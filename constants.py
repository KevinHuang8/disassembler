import math

# Size of game window
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

# The proportion of the non-menu part of the application GUI that the game
# takes up
GAME_WINDOW_PROPORTION = 0.8

# The proportion that the menu takes up from the application GUI
MENU_PROPORTION = 0.1

FONT = ('Courier', 12)

# The spacing between squares in the GUI. Larger = smaller spacing
SPACING = 13

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

# How fast to animate text. Lower = faster
TEXT_SPEED = 15

# Max number of rows and columns allowed
MAX_SIZE = 20
import tkinter as tk

import GameState as gs

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

class Application:
    '''
    Represents the main application window of a dissembler game.
    '''
    def __init__(self, master, init_size=(800,600)):
        '''
        Arguments:
            master: a tk.Tk object that manages the window
            init_size: a tuple of two non-negative integers representing the
            initial size of the game window (width, height) in pixels

        Creates and populates all of the GUI elements of the game.
        '''
        self.master = master
        self.width, self.height = init_size
        self.master.geometry(f'{self.width}x{self.height}')

        self.create_widgets()

        # A GameState object
        self.game_state = gs.GameState()

        self.game_state.add((0, 0), 'red')
        self.game_state.add((1, 1), 'red')
        self.game_state.add((1, 0), 'blue')
        self.game_state.add((4, 4), 'green')
        self.game_state.add((2, 3), 'blue')
        self.game_state.add((1, 1), 'blue')
        self.game_state.add((1, 1), 'green')

        self.draw_game_state(self.game_canvas)

    def mainloop(self):
        self.master.mainloop()

    def create_widgets(self):
        '''
        Creates all of the widgets in the GUI. Consists of 3 main widgets:

        - self.menu_canvas: the canvas which holds the drop-down menu
        - self.game_canvas: the canvas which holds the actual dissembler game
        - self.info_frame: a frame that contains text displayed to the player

        Within inf_frame, there is a label that displays the text.
        '''

        menu_size = self.height * MENU_PROPORTION
        game_size = self.height * (1 - MENU_PROPORTION) * GAME_WINDOW_PROPORTION
        text_size = (self.height - menu_size) * (1 - GAME_WINDOW_PROPORTION)

        self.menu_canvas = tk.Canvas(self.master, width = self.width, 
            height = menu_size)

        self.game_canvas = tk.Canvas(self.master, width = self.width, 
            height = game_size)

        self.info_frame = tk.Frame(self.master, width = self.width,
            height = text_size)

        self.display = tk.Label(self.info_frame, text='asdf', anchor='w',
            font=FONT)

        self.menu_canvas.pack(fill='both')
        self.game_canvas.pack(fill='both')
        self.info_frame.pack(fill='both')

        self.display.pack(fill='both')

    def draw_game_state(self, canvas):
        '''
        Arguments:
            canvas: a tkinter canvas

        Draws the current game state to the canvas.
        '''

        space_size, x, y = self.get_drawing_dimensions(canvas)

        for loc in self.game_state:
            tag = f'{loc[0]}+{loc[1]}'

            if not loc:
                self.canvas.delete(tag)
                continue

            color_stack = self.game_state[loc]

            colored_squares = []
            for i, color in enumerate(color_stack):
                if i > 4:
                    # Colors beyond the 4th appear as black
                    color = 'black'

                if i == 0:
                    modified_tag = (tag, 'outside')
                else:
                    modified_tag = tag
                self.draw_square_in_grid(canvas, space_size, 
                    x + loc[0] * space_size, y + loc[1] * space_size, 
                    color, modified_tag,
                    SPACING + i*INNER_SPACING)

            self.game_canvas.tag_bind(tag, '<Enter>', 
                lambda event, tag=tag: self.on_game_hover(event, tag))
            self.game_canvas.tag_bind(tag, '<Leave>', 
                lambda event, tag=tag: self.on_game_hover(event, tag))

    def get_drawing_dimensions(self, canvas):
        '''
        Arguments:
            canvas: a tkinter canvas

        Computes the square grid where the squares in the dissembler
        game should be drawn relative to the canvas.

        Returns (square_size, startx, starty), where
        'space_size' is the length
        of one square space in the grid, and 'startx' and 'starty' are the pixel
        coordinate of the top left of the grid, relative to the canvas.
        '''
        nrows = self.game_state.nrows()
        ncols = self.game_state.ncols()

        n = max(nrows, ncols)

        width = int(canvas['width'])
        height = int(canvas['height'])

        offset = abs(width - height) / 2

        if width > height:
            x = offset
            y = 0
        else:
            x = 0
            y = offset

        total_length = min(width, height)

        space_size = total_length / n

        return space_size, x, y

    def draw_square_in_grid(self, canvas, space_size, x, y, color, tag,
        spacing=SPACING):
        '''
        Arguments:
            canvas: a tkinter canvas
            space_size: the size of the grid space allocated to the square
            x, y: the pixel coords of the top left of the grid square relative 
            to the canvas
            color: the color to draw the square
            tag: identifying handle of the square in the canvas
            spacing: an integer representing the number of pixels between the
            edge of the square and the edge of the grid space allocated to it

        Draws a square on canvas in a grid space allocated to it, defined by
        'square_size', 'x', and 'y'
        '''
        canvas.create_rectangle(x + spacing, y + spacing, 
            x + space_size - spacing, y + space_size - spacing, fill=color,
            outline=color, width=4, tags=tag)

    def on_game_hover(self, event, tag):
        '''
        Arguments:
            event: a tkinter event
            tag: tag of the item hovered over

        A callback function to highlight the square being hovered over by the
        mouse. Only highlights outermost square.
        '''
        tag_squres = event.widget.find_withtag(tag)
        outside_squares = event.widget.find_withtag('outside')

        item = set(tag_squres).intersection(outside_squares).pop()

        if event.type == '7':  # Enter
            event.widget.itemconfig(item, outline='black', width=4)
        elif event.type == '8': # Leave
            event.widget.itemconfig(item, outline='', width=4)

    def key_handler(self):
        pass

    def on_mouse_click(self):
        pass


root = tk.Tk()
app = Application(root)
app.mainloop()
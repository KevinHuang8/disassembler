import math, cmath
import tkinter as tk

import GameState as gs
import locset as ls
from animator import Animator
from constants import *

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
        self.animator = Animator(self)

        # Whether a game square has been clicked
        self.square_clicked = None
        # Whether a game animation is currently going on
        self.animating = False

        # A GameState object
        self.game_state = gs.GameState()

        self.game_state.add((0, 2), 'red')
        self.game_state.add((1, 2), 'red')
        self.game_state.add((2, 2), 'blue')
        self.game_state.add((3, 2), 'red')
        self.game_state.add((4, 2), 'yellow')
        self.game_state.add((5, 2), 'yellow')
        self.game_state.add((6, 2), 'green')
        self.game_state.add((7, 2), 'yellow')
        self.game_state.add((8, 2), 'green')
        self.game_state.add((9, 2), 'green')
        self.game_state.add((3, 1), 'green')
        self.game_state.add((3, 0), 'green')
        self.game_state.add((3, 3), 'blue')
        self.game_state.add((3, 4), 'blue')
        self.game_state.add((2, 2), 'green')

        self.draw_game_state()

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

        self.game_canvas.bind('<Button-1>', self.on_game_click)

    def draw_game_state(self):
        '''
        Draws the current game state to the game canvas.
        '''

        self.game_canvas.delete('all')

        space_size, x, y = self.get_drawing_dimensions()

        for loc in self.game_state:
            tag = f'{loc[0]}+{loc[1]}'

            try:
                color_queue = self.game_state[loc]
            except KeyError:
                continue
            
            colored_squares = []
            for i, color in enumerate(color_queue):
                if i > 4:
                    # Colors beyond the 4th appear as black
                    color = 'black'

                if i == 0:
                    modified_tag = (tag, 'outside')
                else:
                    modified_tag = tag
                self.draw_square_in_grid(self.game_canvas, space_size, 
                    *self.loc_to_coord(loc), 
                    color, modified_tag,
                    SPACING + i*INNER_SPACING)

            self.game_canvas.tag_bind(tag, '<Enter>', 
                lambda event, tag=tag: self.on_square_hover(event, tag))
            self.game_canvas.tag_bind(tag, '<Leave>', 
                lambda event, tag=tag: self.on_square_hover(event, tag))

            self.game_canvas.tag_bind(tag, '<Button-1>', 
                lambda event, tag=tag: self.on_square_click(event, tag))

    def get_drawing_dimensions(self):
        '''
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

        width = int(self.game_canvas['width'])
        height = int(self.game_canvas['height'])

        offset = int(abs(width - height) / 2)

        if width > height:
            x = offset
            y = 0
        else:
            x = 0
            y = offset

        total_length = min(width, height)

        space_size = total_length // n

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
        canvas.create_polygon(
            [(x + spacing, y + spacing),
            (x + spacing, y + space_size - spacing),
            (x + space_size - spacing, y + space_size - spacing), 
            (x + space_size - spacing, y + spacing)], 
            fill=color, outline='', width=4, tags=tag)

    def on_square_hover(self, event, tag):
        '''
        Arguments:
            event: a tkinter event
            tag: tag of the item hovered over

        A callback function to highlight the square being hovered over by the
        mouse. Only highlights outermost square.
        '''
        if self.square_clicked and self.square_clicked[0] == tag:
            return

        if self.animator.animating:
            return

        tag_squres = event.widget.find_withtag(tag)
        outside_squares = event.widget.find_withtag('outside')

        item = set(tag_squres).intersection(outside_squares).pop()

        if event.type == '7':  # Enter
            event.widget.itemconfig(item, outline='black', width=4)
        elif event.type == '8': # Leave
            event.widget.itemconfig(item, outline='', width=4)

    def on_square_click(self, event, tag):
        '''
        A callback function called when a square with 'tag' gets clicked on 
        by the mouse.
        '''
        if self.animator.animating:
            return

        tag_squres = event.widget.find_withtag(tag)
        outside_squares = event.widget.find_withtag('outside')

        item = set(tag_squres).intersection(outside_squares).pop()

        event.widget.itemconfig(item, outline='black', width=4)

        if not self.square_clicked:
            self.square_clicked = tag, item
            return

        loc1 = self.coord_to_loc(self.game_canvas.coords(
            self.square_clicked[1])[:2])
        loc2 = self.coord_to_loc((event.x, event.y))

        try:
            removed = self.game_state.make_move(loc1, loc2)
        except ValueError:
            # Send a message that the move is invalid!
            if not ls.is_adjacent(loc1, loc2):
                print('Not adjacent!')
            else:
                print("Doesn't remove anything!")
        else:
            direction = ls.orientation(loc1, loc2)
            self.animator.animate_swap(self.square_clicked[0], tag, loc2, 
                direction, removed)

    def key_handler(self):
        pass

    def on_game_click(self, event):
        '''
        A callback function called when the mouse is clicked inside the game
        canvas.
        '''
        if not self.square_clicked or self.animator.animating:
            return

        if not event.widget.find_overlapping(event.x, event.y, 
            event.x, event.y):
            item = self.square_clicked[1]
            event.widget.itemconfig(item, outline='')
            self.square_clicked = None

    def loc_to_coord(self, loc):
        '''
        Arguments:
            loc - a (row, column) location

        Returns the pixel coordinates of the square space corresponding to loc
        relative to the game canvas.
        '''

        space_size, x, y = self.get_drawing_dimensions()

        return x + space_size * loc[0], y + space_size * loc[1]

    def coord_to_loc(self, coord):
        '''
        Arguments:
            coord: a (x, y) pixel coordinate relative to the game canvas

        Returns the corresponding (row, col) location that
        contains the coord.
        '''
        space_size, x, y = self.get_drawing_dimensions()

        row = (coord[0] - x) // space_size
        col = (coord[1] - y) // space_size

        return int(row), int(col)


root = tk.Tk()
app = Application(root)
app.mainloop()
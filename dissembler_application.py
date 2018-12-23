import math, cmath, random
import tkinter as tk
from tkinter.filedialog import askopenfilename
from copy import deepcopy

import GameState as gs
import locset as ls
from animator import Animator
from constants import *

class Application:
    '''
    Represents the main application window of a dissembler game.
    '''
    def __init__(self, master, init_size=(WINDOW_WIDTH, WINDOW_HEIGHT)):
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
        self.create_menu_buttons()
        self.animator = Animator(self)
        self.master.bind('<Key>', self.key_handler)

        # Whether a game square has been clicked
        self.square_clicked = None

        # A GameState object
        self.game_state = gs.GameState()
        # A stack of game states, for the purpose of undoing moves
        self.state_stack = []
        # Number of moves made, undos do not reset
        self.moves = 0

        self.send_message('Hello! To start playing, please load a puzzle file.'+
            ' Many pre-built examples are included.' +
            ' For more info, such as keybinds, see readme.txt.')

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

        self.display_text = tk.StringVar()
        self.display = tk.Message(self.info_frame,
            textvariable=self.display_text, anchor='w',
            font=FONT, width=self.width, justify='left')

        self.menu_canvas.pack(expand='yes', fill='both')
        self.game_canvas.pack(expand='yes', fill='both')
        self.info_frame.pack(expand='yes', fill='both')

        self.display.pack(expand='yes', fill='both')

        self.game_canvas.bind('<Button-1>', self.on_game_click)

    def create_menu_buttons(self):
        '''
        Creates the buttons bound to the menu canvas.
        '''

        width = int(self.menu_canvas['width'])
        height = int(self.menu_canvas['height'])

        button_diameterx = int((width - 4 * (width / SPACING)) / 6)
        button_diametery = int((height - 2 * (height / SPACING)) / 2)

        button_width = int(button_diameterx*113/400)
        button_height = int(button_diametery*10/100)

        load_button = tk.Button(self.master, text='Load', 
            command=self.prompt_load, width=button_width, height=button_height)

        self.menu_canvas.create_window(width / SPACING + button_diameterx,
            height / SPACING + button_diametery, window=load_button,
            tag='load')

        undo_button = tk.Button(self.master, text='Undo', 
            command=self.undo_move, width=button_width, height=button_height)

        self.menu_canvas.create_window(2*(width / SPACING) + 3*button_diameterx,
            height / SPACING + button_diametery, window=undo_button,
            tag='undo')

        restart_button = tk.Button(self.master, text='Restart', 
            command=self.restart, width=button_width, height=button_height)

        self.menu_canvas.create_window(3*(width / SPACING) + 5*button_diameterx,
            height / SPACING + button_diametery, window=restart_button,
            tag='restart')

    def load(self, filename, game_state):
        '''
        Loads a dissembler file from 'filename' into 'game_state'.

        Returns the updated game state.
        ''' 
        color_dict = {}

        with open(filename, 'r') as file:
            line = file.readline()

            if file.readline():
                raise IOError('The contents of the file need to be on one ' +
                    'line. See readme.txt for more info on proper input.')

            for r, row in enumerate(line.split(' ')):
                if r > MAX_SIZE:
                    raise IOError('The size of the puzzle is limited to '+
                        f'{MAX_SIZE}.')

                squares = []
                it = iter(row)

                for elem in it:
                    if elem == '|':
                        square = ''
                        elem = next(it)
                        try:
                            while elem != '|':
                                if elem == '.':
                                    raise IOError('"." cannot be used inside' +
                                        ' a pair of "|". See readme.txt ' + 
                                        'for more info on proper input.')
                                square += elem
                                elem = next(it)
                        except StopIteration as e:
                            raise IOError('"|" symbols must be in pairs. ' + 
                                'See readme.txt for more info on ' +
                                'proper input.') from e

                        squares.append(square)
                    else:
                        squares.append(elem)

                for c, square in enumerate(squares):
                    if c > MAX_SIZE:
                        raise IOError('The size of the puzzle is limited to ' +
                            f'{MAX_SIZE}.')
                    for i in square:
                        if i == '.':
                            break
                        if i not in color_dict:
                            color_dict[i] = self.random_color()
                        game_state.add((c, r), color_dict[i])

        return game_state

    def prompt_load(self):
        '''
        Prompts the user to load a file.
        '''
        filename = askopenfilename()
        if not filename:
            return
        new_game_state = gs.GameState()

        try:
            self.load(filename, new_game_state)
        except IOError as e:
            self.send_message('Your file is not a valid input: ' + str(e), 
                'red')
            return

        self.game_state = new_game_state
        self.state_stack = []
        self.moves = 0

        self.state_stack.append(deepcopy(self.game_state))

        self.display_text.set('')
        self.animator.cancel_text_animation(self.display_text)
        self.animator.cancel_animation()
        self.draw_game_state()
                       
    def random_color(self):
        """
        Returns a random string in the form of #RRGGBB, representing a color 
        code in hex form.
        """
        color = '#'
        for i in range(6):
            hex_code = random.randint(0, 15)
            # must do [2:] b/c hex starts w/ '0x'
            color += hex(hex_code)[2:]

        return color

    def draw_game_state(self):
        '''
        Draws the current game state to the game canvas.
        '''
        self.game_canvas.delete('all')

        space_size, x, y = self.get_drawing_dimensions()

        self.spacing = space_size / SPACING

        for loc in self.game_state:
            tag = f'{loc[0]}+{loc[1]}'

            try:
                color_queue = self.game_state[loc]
            except KeyError:
                continue
            
            colored_squares = []
            for i, color in enumerate(color_queue):
                if i > 3:
                    # Colors beyond the 4th appear as black
                    color = 'black'

                if i == 0:
                    modified_tag = (tag, 'outside')
                else:
                    modified_tag = tag
                self.draw_square_in_grid(self.game_canvas, space_size, 
                    *self.loc_to_coord(loc), 
                    color, modified_tag,
                    self.spacing + i*(0.25*(space_size/2 - self.spacing - 3)))

            self.game_canvas.tag_bind(tag, '<Enter>', 
                lambda event, tag=tag: self.on_square_hover(event, tag))
            self.game_canvas.tag_bind(tag, '<Leave>', 
                lambda event, tag=tag: self.on_square_hover(event, tag))

            self.game_canvas.tag_bind(tag, '<Button-1>', 
                lambda event, tag=tag: self.on_square_click(event, tag))

        # Move counter
        self.game_canvas.create_text(self.width - FONT[1]*4, 
            FONT[1], font=FONT, text=f'Moves: {self.moves}')

    def get_drawing_dimensions(self):
        '''
        Computes the rectangular grid where the squares in the dissembler
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

        canvas_ratio = width / height

        game_ratio = nrows / ncols

        if game_ratio > canvas_ratio:
            # Widths are matching
            r = (width * ncols) / (height * nrows)
            x = 0
            y = int(height * (1 - r)) // 2
            space_size = width / nrows
        elif game_ratio <= canvas_ratio:
            # Heights are matching
            r = (height * nrows) / (width * ncols)
            x = int(width * (1 - r)) // 2
            y = 0
            space_size = height / ncols

        return space_size, x, y

    def draw_square_in_grid(self, canvas, space_size, x, y, color, tag,
        spacing):
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

    def loc_to_coord(self, loc):
        '''
        Arguments:
            loc - a (row, column) location

        Returns the pixel coordinates of the square space corresponding to loc
        relative to the game canvas.
        '''

        space_size, x, y = self.get_drawing_dimensions()

        locx = loc[0] - self.game_state.minrow
        locy = loc[1] - self.game_state.mincol

        return x + space_size * locx, y + space_size * locy

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

        row -= self.game_state.minrow
        col -= self.game_state.mincol

        return int(row), int(col)

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

        # Clicked on second square

        loc1 = self.coord_to_loc(self.game_canvas.coords(
            self.square_clicked[1])[:2])
        loc2 = self.coord_to_loc((event.x, event.y))

        try:
            removed = self.game_state.make_move(loc1, loc2)
        except ValueError:
            self.send_message(self.get_swap_error_msg(loc1, loc2), 'red')
        else:
            self.on_swap(self.square_clicked[0], tag, loc1, loc2, removed)
            game_state_copy = deepcopy(self.game_state)
            self.state_stack.append(game_state_copy)

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

    def key_handler(self, event):
        if event.keysym == 'u':
            self.undo_move()

        elif event.keysym == 'l':
            self.prompt_load()

        elif event.keysym == 'r':
            self.restart()

        elif event.keysym == 'q':
            self.master.destroy()

    def undo_move(self):
        '''
        Reverts the game state to the previous state on the game_stack.
        '''
        self.animator.cancel_animation()
        self.animator.cancel_text_animation(self.display_text)

        try:
            self.game_state = deepcopy(self.state_stack[-2])
            self.state_stack.pop()
        except IndexError:
            # Nothing to undo
            return

        self.draw_game_state()

    def restart(self):
        '''
        Restarts the puzzle
        '''
        self.moves = 0

        self.animator.cancel_animation()
        self.animator.cancel_text_animation(self.display_text)

        self.game_state = self.state_stack[0]
        self.state_stack = [deepcopy(self.game_state)]
        self.draw_game_state()

    def send_message(self, msg, color='black'):
        '''
        Arguments:
            msg: a string

        Displays an message on the GUI
        '''
        self.display_text.set('')
        self.display['foreground'] = color
        self.animator.animate_text(msg, self.display_text)

    def get_swap_error_msg(self, loc1, loc2):
        '''
        Arguments:
            loc1, loc2: two location tuples

        Called when a move swap is invalid. Returns the error message 
        corresponding to the invalid move of loc1 and loc2.
        '''

        if not ls.is_adjacent(loc1, loc2):
            return 'Your move needs to swap two adjacent squares!'
        else:
            return 'Your move needs to connect at least 3 squares of the same'+\
            ' color!'

    def on_swap(self, tag1, tag2, loc1, loc2, removed):
        '''
        Arguments:
            tag1, tag2: two strings referring to the squares that were just
            swapped
            loc1, loc2: location tuples corresponding to the squares
            removed: a locset of removed locations

        Called when a valid swap occurs. Resolves the swap.
        '''
        self.moves += 1

        self.display_text.set('')

        direction = ls.orientation(loc1, loc2)
        self.animator.animate_swap(tag1, tag2, loc2, 
            direction, removed)

    def after_swap(self, tag1, tag2, removed):
        '''
        Arguments:
            tag1, tag2: two canvas tags corresponding to squares that were
            just succesfully swapped.
            removed: a set of locations that had their colors stripped

        Called after the swaping animation is done. Resolves any actions
        that are needed after a swap.
        '''
        # Unclick
        self.game_canvas.itemconfig(tag1, outline='')
        self.game_canvas.itemconfig(tag2, outline='')
        self.square_clicked = None

        self.animator.animate_removal(removed, 0)

    def check_victory(self):
        '''
        If the game has been won, activate the victory splash screen.
        '''

        if not self.game_state:
            self.game_canvas.delete('all')

            x = int(self.game_canvas['width']) / 2
            y = int(self.game_canvas['height']) / 2

            victory_image = tk.PhotoImage(file=VICTORY_IMAGE)

            width = victory_image.width()
            height = victory_image.height()

            largest_dim = max(width, height)
            smallest_window = min(x*2, y*2)

            scaling_factor = int(largest_dim / smallest_window) + 1
            victory_image = victory_image.subsample(50)

            self.game_canvas.image = victory_image
            self.game_canvas.create_image(x, y, image=victory_image, 
                tag='photo')
            self.animator.animate_victory(smallest_window, victory_image)

            self.game_canvas.create_text(x, y, text='You Win!', 
                font=('Courier', 44))


root = tk.Tk()
app = Application(root)
app.mainloop()
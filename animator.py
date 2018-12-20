import cmath
from constants import *

class Animator:
    '''
    Helper class with methods that animate the squares in the main GUI.
    '''

    def __init__(self, main):
        self.main = main
        self.game_canvas = main.game_canvas

        # If the game canvas is being animated
        self.animating = False

        # If text is being animated
        self.text_animating = False

    def animate_swap(self, tag1, tag2, loc2, direction, removed):
        '''
        Arguments:
            tag1, tag2: canvas tags corresponding to the two squares to swap
            loc2: the (row, col) location of the square corresponding to tag2
            direction: a string, either 'N','E','S', or 'W', depending on 
            the relative orientation of tag2 to tag2
            removed: a set of locations that had their colors stripped

        Animates the swapping of squares tag1 and tag2.
        '''
        self.animating = True

        if direction == 'E':
            self.game_canvas.move(tag1, SWAP_SPEED, 0)
            self.game_canvas.move(tag2, -SWAP_SPEED, 0)
        elif direction == 'W':
            self.game_canvas.move(tag2, SWAP_SPEED, 0)
            self.game_canvas.move(tag1, -SWAP_SPEED, 0)
        elif direction == 'N':
            self.game_canvas.move(tag1, 0, SWAP_SPEED)
            self.game_canvas.move(tag2, 0, -SWAP_SPEED)
        elif direction == 'S':
            self.game_canvas.move(tag2, 0, SWAP_SPEED)
            self.game_canvas.move(tag1, 0, -SWAP_SPEED)
        
        space_coord = self.main.loc_to_coord(loc2)
        square_coord = (space_coord[0] + self.main.spacing, 
            space_coord[1] + self.main.spacing)

        item = self.game_canvas.find_withtag(tag1)
        if type(item) is tuple:
            item = item[0]

        distx, disty = self.distance(square_coord,
            self.game_canvas.coords(item)[:2])

        if abs(distx) < SWAP_SPEED and abs(disty) < SWAP_SPEED:
            self.animating = False
            self.game_canvas.move(tag1, distx, disty)
            self.game_canvas.move(tag2, -distx, -disty)
            
            self.main.after_swap(tag1, tag2, removed)
            
            return

        self.game_task = self.game_canvas.after(15, lambda tag1=tag1, tag2=tag2, 
            loc2=loc2, direction=direction, removed=removed: 
            self.animate_swap(tag1, tag2, loc2, direction, removed))

    def animate_removal(self, removed, i):
        '''
        Arguments:
            removed: a set of locations that had their colors stripped
            i: number of iterations
        '''
        self.animating = True

        space_size, _x, _y = self.main.get_drawing_dimensions()

        for loc in removed:
            xspace, yspace = self.main.loc_to_coord(loc)

            items = self.game_canvas.find_overlapping(xspace, yspace, 
                xspace + space_size, yspace + space_size)

            for item in items:
                # Don't animate inside color squares
                if len(self.game_canvas.gettags(item)) == 1:
                    continue

                coords = self.game_canvas.coords(item)
                new_coords = []

                # coordinate of center of rectangle
                offset = ((coords[0] + coords[4]) / 2) + \
                ((coords[1] + coords[3]) / 2)*1j

                # Multiply coordinates by a complex number to rotate
                it = iter(coords)
                for coord in it:
                    x, y = coord, next(it)
                    complex_coord = x + y*1j
                    transformed = (complex_coord - offset)*cmath.exp(
                        1j*ROTATION_SPEED)*SHRINK_FACTOR + offset

                    new_coords.append((transformed.real)) 
                    new_coords.append((transformed.imag))

                self.game_canvas.coords(item, *new_coords)

        if i > REMOVE_TIME:
            self.animating = False
            self.main.draw_game_state()
            self.main.check_victory()
            return

        self.game_task = self.game_canvas.after(15, lambda i=i: 
            self.animate_removal(removed, i + 1))

    def animate_victory(self, length, image):
        '''
        Arguments:
            length: the pixel length at which the photo should stop growing
            image: the PhotoImage object to animate

        Animate the victory trophy appearing.
        '''
        self.animating = True

        if max(image.width(), image.height()) * IMAGE_GROWTH_FACTOR[0] / \
        IMAGE_GROWTH_FACTOR[1] > length:
            self.animating = False
            return

        image = image.zoom(IMAGE_GROWTH_FACTOR[0])
        image = image.subsample(IMAGE_GROWTH_FACTOR[1])

        self.game_canvas.image = image
        self.game_canvas.itemconfig('photo', image=image)
        
        self.game_canvas.after(15, 
            lambda: self.animate_victory(length, image))

    def animate_text(self, text, text_variable):
        '''
        Arguments:
            text: the text to animate
            text_variable: a tkinter StringVar to update 

        Animate the appearance to text.
        '''
        self.cancel_text_animation(text_variable)

        self.text_animating = True
        self._animate_text(text, text_variable)

    def _animate_text(self, text, text_variable):
        '''
        The helper function to animate_text() that carries out the recursive
        calls.
        '''
        try:
            letter = text[0]
        except IndexError:
            # No more text to animate
            self.text_animating = False
            return

        text = text[1:]

        curr_text = text_variable.get()

        curr_text += letter

        text_variable.set(curr_text)

        self.text_task = self.main.display.after(TEXT_SPEED, 
            lambda: self._animate_text(text, text_variable))

    def cancel_animation(self):
        '''
        Stop any animations on the game canvas, if there are any.
        Doesn't stop the victory animation.
        '''
        if self.animating:
            self.animating = False
            self.game_canvas.after_cancel(self.game_task)

            self.main.square_clicked = None

    def cancel_text_animation(self, text_variable):
        '''
        Stops any text animations, if any. Resets the text_variable display.
        '''
        if self.text_animating:
            self.main.display.after_cancel(self.text_task)
            text_variable.set('')

    def distance(self, coord1, coord2):
        '''
        Arguments:
            coord1, coord2: (x, y) pixel coordinates

        Returns (x, y) distance between coord1 and coord2.
        '''

        return (coord1[0] - coord2[0]), (coord1[1] - coord2[1])
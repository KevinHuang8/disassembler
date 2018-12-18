import tkinter as tk

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

	def mainloop(self):
		self.master.mainloop()

	def create_widgets(self):
		'''
		Creates all of the widgets in the GUI. Consists of 3 main widgets:

		- self.menu_canvas: the canvas which holds the drop-down menu
		- self.game_canvas: the canvas which holds the actual dissembler game
		- self.info_frame: a frame that contains text displayed to the player
		'''
		self.menu_canvas = tk.Canvas(self.master, width=self.width, 
			height=self.height/6)

		self.game_canvas = tk.Canvas(self.master, width=self.width, 
			height=self.height/2)

		self.info_frame = tk.Frame(self.master, width=self.width, 
			height=self.height/3)

		self.menu_canvas.pack(fill='both')
		self.game_canvas.pack(fill='both')
		self.info_frame.pack(fill='both')

	def key_handler(self):
		pass

	def on_mouse_click(self):
		pass


root = tk.Tk()
app = Application(root)
app.mainloop()
import tkinter as tk

class Application:
	'''
	Represents the main application window of a dissembler game.
	'''
	def __init__(self, master):
		'''
		Arguments:
			master: a tk.Tk object that manages the window

		Creates and populates all of the GUI elements of the game.
		'''
		self.master = master

		self.create_widgets()
		self.populate_widgets()

	def mainloop(self):
		self.master.mainloop()

	def create_widgets(self):
		pass

	def populate_widgets(self):
		pass

	def key_handler(self):
		pass

	def on_mouse_click(self):
		pass


root = tk.Tk()
app = Application(root)
app.mainloop()
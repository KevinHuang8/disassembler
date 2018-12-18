from collections import defaultdict

class GameState:
	def __init__(self):
		self.loc_to_color = defaultdict(list)
		self.color_to_loc = defaultdict(set)

	def add(self, loc, color):
		'''
		Arguments:
			loc: a (x, y) tuple describing a location
			color: a string representing a valid tkinter color

		Associates 'loc' with 'color'. Note, a 'loc' can have
		multiple colors associated with it, so a 'loc' is really associated
		with a stack of color, with the topmost element being the current color.
		'''
		color_stack = self.loc_to_color[loc]

		try:
			old_color = color_stack[-1]
		except IndexError:
			pass
		else:
			self.color_to_loc[old_color].remove(loc)

		color_stack.append(color)
		self.color_to_loc[color].add(loc)

	def strip(self, loc):
		'''
		Arguments:
			loc: a (x, y) tuple describing a location

		Removes the topmost color on the stack of colors associated with loc.
		'''
		color_stack = self.loc_to_color[loc]

		if not color_stack:
			raise ValueError('Loc is empty!')

		color = color_stack.pop()
		self.color_to_loc[color].remove(loc)

		try:
			new_color = color_stack[-1]
		except IndexError:
			pass
		else:
			self.color_to_loc[new_color].add(loc)

	def swap(self, loc1, loc2):
		'''
		Arguments:
			loc1, loc2: two (x, y) tuples describing locations

		Swaps loc1 and loc2
		'''
		if not self.loc_to_color[loc1] or not self.loc_to_color[loc2]:
			raise ValueError('Loc is empty!')

		color1 = self.loc_to_color[loc1][-1]
		color2 = self.loc_to_color[loc2][-1]

		self.color_to_loc[color2].remove(loc2)
		self.color_to_loc[color1].add(loc2)
		self.color_to_loc[color1].remove(loc1)
		self.color_to_loc[color2].add(loc1)

		temp = self.loc_to_color[loc1]
		self.loc_to_color[loc1] = self.loc_to_color[loc2]
		self.loc_to_color[loc2] = temp

		

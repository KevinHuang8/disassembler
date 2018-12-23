To start the GUI, run "dissembler_application.py"

The GUI supports a more advanced version of the dissembler game, supporting multiple colors in one square.
In this case, the outermost color of a square is its current color, and must be removed first.

Loading a puzzle requires a plain text file with only one line. A consecutive sequence of non-space characters
represents a row. A '.' character represents a blank space, and any other single character represents a color.
All squares with the same character will have the same color, though the exact color will be chosen
randomly every time the puzzle is loaded. If two different colors look too similar, it might be better
to reload the file.

To specify a square with multiple colors, wrap the square in a pair of '|'. For example, '|abc|' will
specify a square with 3 colors: a, b, and c, with a being the top color.

Ex: 'ab.|ca|b c.a|aba|.' specifies a puzzle like this:

Row 1: [A]  [B]      [BLANK]    [C then A]      [B]
Row 2: [C]  [Blank]    [A]   [A then B then A]  [BLANK]

Keybindings:
q - Exit
u - Undo
r - Restart
l - Load

Also, undos do not remove a move from your move count.
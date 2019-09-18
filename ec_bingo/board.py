from collections import namedtuple
from io import StringIO

SquareInfo = namedtuple('SquareInfo', 'data has_piece')

class Bingo:
	WIDTH = 5
	HEIGHT = 5

	H1 = HEIGHT + 1
	H2 = HEIGHT + 2
	SIZE = HEIGHT * WIDTH
	SIZE1 = H1 * WIDTH

	COL_I = {c: i for i, c in enumerate('BINGO')}
	COL_NAMES = {i: c for c, i in COL_I.items()}
	FLIP_ROW = range(HEIGHT)[::-1]

	def __init__(self):
		self.board = 0
		self['N', 3] = 1  # free space
		self.data = {}

	reset = __init__

	def is_playable(self, col, row):
		"""return whether the square has room"""
		return not self[col, row].has_piece

	def has_won(self):
		board = self.board
		y = board & (board >> self.HEIGHT)
		if (y & (y >> 2 * self.HEIGHT)) != 0:  # diagonal \
			return True
		y = board & (board >> self.H1)
		if (y & (y >> 2 * self.H1)) != 0:  # horizontal -
			return True
		y = board & (board >> self.H2)
		if (y & (y >> 2 * self.H2)) != 0:  # diagonal /
			return True
		y = board & (board >> 1)
		return (y & (y >> 2)) != 0  # vertical |

	def __setitem__(self, pos, value):
		mask = self._mask(pos)
		if value:
			self.board |= mask
		else:
			self.board &= ~mask

	def __getitem__(self, pos):
		mask = self._mask(pos)
		return SquareInfo(self.data.get(pos), self.board & mask != 0)

	@classmethod
	def _mask(cls, pos):
		col, row = pos
		col, row = cls.COL_I[col], cls.FLIP_ROW[row - 1]
		i = col * cls.H1 + row
		return 1 << i

	def __str__(self):
		buf = StringIO()

		buf.write('  ')
		for w in range(self.WIDTH):
			# column indexes
			buf.write(self.COL_NAMES[w])
			buf.write(' ')

		buf.write('\n')

		for h in range(self.HEIGHT - 1, -1, -1):
			buf.write(str(self.HEIGHT - h))
			for w in range(h, self.SIZE1, self.H1):
				mask = 1 << w
				buf.write(' ')
				buf.write('X' if self.board & mask != 0 else '.')
			buf.write('\n')

		return buf.getvalue()

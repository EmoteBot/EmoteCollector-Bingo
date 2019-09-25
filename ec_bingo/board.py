# SPDX-License-Identifier: BlueOak-1.0.0

from collections import namedtuple

SquareInfo = namedtuple('SquareInfo', 'data has_piece')

class Bingo:
	WIDTH = 5
	HEIGHT = 5

	SIZE = HEIGHT * WIDTH
	SQUARES = SIZE - 1  # free space

	COL_I = {c: i for i, c in enumerate('BINGO')}
	COL_NAMES = {i: c for c, i in COL_I.items()}

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

		horiz_mask = self.HORIZ_MASK
		for _ in range(self.HEIGHT):
			if board & horiz_mask == horiz_mask:
				return True
			horiz_mask <<= 1

		vert_mask = self.VERT_MASK
		for _ in range(self.WIDTH):
			if board & vert_mask == vert_mask:
				return True
			vert_mask <<= self.HEIGHT

		if board & self.DIAGONAL_TOP_LEFT == self.DIAGONAL_TOP_LEFT:
			return True
		if board & self.DIAGONAL_BOTTOM_LEFT == self.DIAGONAL_BOTTOM_LEFT:
			return True

		return False

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
		col, row = cls.COL_I[col], row - 1
		i = col * cls.HEIGHT + row
		return 1 << i

	@classmethod
	def _init_masks(cls):
		import functools
		import itertools
		import operator

		positions = list(itertools.product('BINGO', range(1, 6)))
		masks = {pos: cls._mask(pos) for pos in positions}

		bit_or = functools.partial(functools.reduce, operator.or_)

		cls.HORIZ_MASK = bit_or(masks[col, 1] for col in 'BINGO')
		cls.VERT_MASK = bit_or(masks['B', i] for i in range(1, 6))

		cls.DIAGONAL_TOP_LEFT = bit_or(masks['BINGO'[i - 1], i] for i in range(1, 6))
		cls.DIAGONAL_BOTTOM_LEFT = bit_or(masks['BINGO'[5 - i], i] for i in range(1, 6)[::-1])

	def __str__(self):
		from io import StringIO
		buf = StringIO()

		buf.write('  ')
		for w in range(self.WIDTH):
			# column indexes
			buf.write(self.COL_NAMES[w])
			buf.write(' ')

		buf.write('\n')

		for h in range(1, self.HEIGHT + 1):
			buf.write(str(h))
			for w in 'BINGO':
				buf.write(' ')
				buf.write('X' if self[w, h] else '.')
			if h != self.HEIGHT:  # skip writing the newline at the end
				buf.write('\n')

		return buf.getvalue()

Bingo._init_masks()

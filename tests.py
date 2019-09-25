import contextlib
import itertools
import random

from ec_bingo.board import Bingo

def test_no_win():
	b = Bingo()
	for c in 'BING':
		b[c, 1] = 1
	assert not b.has_won()

	b = Bingo()
	b['B', 1] = 1
	b['I', 2] = 1
	b['G', 4] = 1
	assert not b.has_won()

	for _ in range(50):
		b = Bingo()
		squares = list(itertools.product('BINGO', range(1, 6)))
		squares.remove(('N', 3))
		random.shuffle(squares)
		for _ in range(4):
			square = squares.pop()
			print(square)
			b[square] = 1
		assert not b.has_won()

def test_horiz():
	for row in range(1, 6):
		b = Bingo()
		for col in 'BINGO':
			b[col, row] = 1
		assert b.has_won()

def test_vert():
	for col in 'BINGO':
		b = Bingo()
		for row in range(1, 6):
			b[col, row] = 1
		assert b.has_won()

def test_diag():
	b = Bingo()
	for i in range(1, 6):
		b['BINGO'[i - 1], i] = 1
	assert b.has_won()

	b = Bingo()
	for i in range(1, 6):
		b['BINGO'[5 - i], i] = 1
	assert b.has_won()

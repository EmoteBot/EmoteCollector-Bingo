import asyncio
import base64
import functools
import io
import json
import random
import operator
import os
import sys
import textwrap
from pathlib import Path

import aiohttp
import aioec
from PIL import Image, ImageDraw, ImageFont

from .board import Bingo

COORDS = {'B': [(284, 287), (284, 552), (284, 817), (284, 1081), (284, 1347)],
          'I': [(548, 287), (548, 552), (548, 817), (548, 1081), (548, 1347)],
          'N': [(813, 287), (813, 552), (813, 1081), (813, 1347)],
          'G': [(1078, 287), (1078, 552), (1078, 817), (1078, 1081), (1078, 1347)],
          'O': [(1342, 287), (1342, 552), (1342, 817), (1342, 1081), (1342, 1347)]}

HERE = Path(__file__).parent

def download(emote_name):
    async def read(name):
        async with \
            aiohttp.ClientSession() as sess, \
            aioec.Client() as client, \
            sess.get((await client.emote(emote_name)).url) as resp \
        :
            return await resp.read()
    try:
        return asyncio.get_event_loop().run_until_complete(read(emote_name))
    except aioec.NotFound:
        print(f'Emote "{emote_name}" not found.', file=sys.stderr)
        sys.exit(2)

def draw_board(cats):
    font = ImageFont.truetype(str(HERE / "arialbd.ttf"), size=44)
    with Image.open(HERE / "bingo_board_base.png") as img:
        draw = ImageDraw.Draw(img)
        for c, (x, y) in zip(cats, functools.reduce(operator.concat, COORDS.values())):
            draw.multiline_text((x, y), "\n".join(textwrap.wrap(c, 10)), font=font, fill=(0, 0, 0))
    return img

def render(board_data):
    img = draw_board(board_data['categories'])
    marks = board_data['emotes'].items()
    mark(img, ((point, base64.b64decode(img.encode('ascii'))) for point, img in marks))
    return img

def parse_point(point):
    col, row = point
    return col, int(row)

def mark(img, marks):
    for point, eimg in marks:
        col, row = parse_point(point)
        point = COORDS[col][row - 1]

        eimg = Image.open(io.BytesIO(eimg)).convert('RGBA')
        eimg = eimg.resize((256, 256))
        img.paste(eimg, point, eimg)

def new():
    with open(HERE / "bingo_categories.txt") as f:
        cats = list(map(str.rstrip, f))
    random.shuffle(cats)

    board = Bingo()
    board.data = {'categories': cats[:-26:-1], 'emotes': {}}
    return vars(board)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print(f"""\
Usage:
	{sys.argv[0]} new > board.json
	{sys.argv[0]} mark <point> <name> < board.json > new-board.json
	{sys.argv[0]} unmark <point> < board.json > new-board.json
	{sys.argv[0]} render < board.json > board.png

Creates a new bingo board for use with Emote Collector,
or modifies a point on an existing board.

Mark and unmark read board data as JSON from stdin and writes board data to stdout.
New takes no arguments and no input, and writes board data to stdout.
Render reads board data from stdin and writes a PNG image to stdout.
""", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == 'new':
        json.dump(new(), sys.stdout)
        sys.exit(0)
    if sys.argv[1] not in ('render', 'mark', 'unmark'):
        print("Unrecognized argument(s):", *sys.argv, file=sys.stderr)
        sys.exit(1)

    board_data = json.load(sys.stdin)

    if sys.argv[1] == 'render':
        img = render(board_data['data'])
        img.save(sys.stdout.buffer, 'png')
        sys.exit(0)

    try:
        _, _, point, *rest = sys.argv
    except ValueError:
        print("Not enough arguments supplied.", file=sys.stderr)
        sys.exit(1)
    if point == 'N3':
        print('Point may not be "N3".', file=sys.stderr)
        sys.exit(1)

    board = Bingo()
    vars(board).update(board_data)

    col, row = parse_point(point)
    if sys.argv[1] == 'unmark':
        board[col, row] = 0
        del board.data['emotes'][point]
    else:  # mark
        try:
            emote, = rest
        except ValueError:
            print("Not enough arguments supplied.", file=sys.stderr)
            sys.exit(1)
        board[col, row] = 1
        board.data['emotes'][point] = base64.b64encode(download(emote)).decode('ascii')

    json.dump(vars(board), sys.stdout)
    sys.exit(0)

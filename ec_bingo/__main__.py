import functools

COORDS = {'b': [(284, 287), (284, 552), (284, 817), (284, 1081), (284, 1347)],
          'i': [(548, 287), (548, 552), (548, 817), (548, 1081), (548, 1347)],
          'n': [(813, 287), (813, 552), (813, 1081), (813, 1347)],
          'g': [(1078, 287), (1078, 552), (1078, 817), (1078, 1081), (1078, 1347)],
          'o': [(1342, 287), (1342, 552), (1342, 817), (1342, 1081), (1342, 1347)]}

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print("""python -m ec_bingo <new|mark <point> <name>>

Creates a new bingo board for use with Emote Collector,
or marks a point on an existing board.

Or, marks a point on an existing board from stdin.
Boards will be written to stdout.
""", file=sys.stderr)
        sys.exit(1)

    from PIL import Image, ImageDraw, ImageFont
    if sys.argv[1] == 'new':
        import operator
        import textwrap
        import pathlib
        import random
        ldir = pathlib.Path(__file__).parent
        font = ImageFont.truetype(str(ldir / "arialbd.ttf"), size=44)
        with open(ldir / "bingo_categories.txt") as f:
            cats = f.readlines()
        with Image.open(ldir / "bingo_board_base.png") as img:
            draw = ImageDraw.Draw(img)
            random.shuffle(cats)
            for x, y in functools.reduce(operator.concat, COORDS.values()):
                c = cats.pop()
                draw.multiline_text((x, y), "\n".join(textwrap.wrap(c, 10)), font=font, fill=(0, 0, 0))
            img.save(sys.stdout.buffer, "png")
        sys.exit(0)
    if sys.argv[1] != 'mark':
        print("Unrecognized argument(s):", *sys.argv, file=sys.stderr)
        sys.exit(1)

    try:
        _, _, point, emoji = sys.argv
    except ValueError:
        print("Not enough arguments supplied.", file=sys.stderr)
        sys.exit(1)
    if point == 'n3':
        print('Point may not be "n3".', file=sys.stderr)
        sys.exit(1)
    import aiohttp
    import asyncio
    import aioec
    import os
    import io

    a, b = point
    point = COORDS[a][int(b)-1]

    with Image.open(sys.stdin.buffer) as img:
        loop = asyncio.get_event_loop()
        client = aioec.Client()
        try:
            emoji = loop.run_until_complete(client.emote(emoji))
        except aioec.NotFound:
            print("Didn't find any emote by that name.", file=sys.stderr)
            sys.exit(1)
        async def read(uri):
            async with aiohttp.ClientSession() as sess, sess.get(uri) as resp:
                return await resp.read()
        eimg = Image.open(io.BytesIO(loop.run_until_complete(read(emoji.url)))).convert('RGBA')
        eimg = eimg.resize((256, 256))
        img.paste(eimg, point, eimg)
        img.save(sys.stdout.buffer, "png")

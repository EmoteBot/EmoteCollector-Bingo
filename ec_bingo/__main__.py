import functools

COORDS = {'b': [(284, 287), (284, 552), (284, 817), (284, 1081), (284, 1347)],
          'g': [(1078, 287), (1078, 552), (1078, 817), (1078, 1081), (1078, 1347)],
          'i': [(548, 287), (548, 552), (548, 817), (548, 1081), (548, 1347)],
          'n': [(813, 287), (813, 552), (813, 1081), (813, 1347)],
          'o': [(1342, 287), (1342, 552), (1342, 817), (1342, 1081), (1342, 1347)]}

q = []

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print("""python -m ec_bingo <new|mark <point> <name>>

Creates a new bingo board for use with Emote Collector,
or marks a point on an existing board.

Or, marks a point on an existing board.
You can specify a path under the env var ECBINGOBOARD
or if left unset, searches for one in the current working
directory.
""")
        sys.exit(1)

    from PIL import Image, ImageDraw, ImageFont
    if sys.argv[1] == 'new':
        import pathlib
        import random
        import textwrap
        print("Generating...")
        ldir = pathlib.Path(__file__).parent
        font = ImageFont.truetype(str(ldir / "arialbd.ttf"), size=44)
        with open(ldir / "bingo_categories.txt") as f:
            cats = f.readlines()
        with Image.open(ldir / "bingo_board_base.png") as img:
            draw = ImageDraw.Draw(img)
            for x, y in functools.reduce(lambda x, y: x+y, COORDS.values()):
                c = random.choice(cats)
                cats.remove(c)
                draw.multiline_text((x, y), "\n".join(textwrap.wrap(c, 10)), font=font, fill=(0, 0, 0))
            img.save("./output_board.png", "png")
        print("saved to `output_board.png`")
        sys.exit(0)
    if sys.argv[1] != 'mark':
        print("Unrecognized argument(s):", *sys.argv)
        sys.exit(1)

    try:
        _, _, point, emoji = sys.argv
    except ValueError:
        print("Not enough arguments supplied.")
        sys.exit(1)
    assert point != 'n3'
    print("One moment...")
    import aiohttp
    import asyncio
    import aioec
    import os
    import io

    a, b = point
    point = COORDS[a][int(b)-1]

    file = os.environ.get('ECBINGOBOARD', 'output_board.png')
    with Image.open(file) as img:
        loop = asyncio.get_event_loop()
        client = aioec.Client()
        try:
            emoji = loop.run_until_complete(client.emote(emoji))
        except aioec.NotFound:
            print("Didn't find any emote by that name.")
            sys.exit(1)
        async def read(uri):
            async with aiohttp.ClientSession() as sess, sess.get(uri) as resp:
                return await resp.read()
        eimg = Image.open(io.BytesIO(loop.run_until_complete(read(emoji.url)))).convert('RGBA')
        eimg = eimg.resize((256, 256))
        img.paste(eimg, point, eimg)
        img.save("output_board.png", "png")
        print("done")

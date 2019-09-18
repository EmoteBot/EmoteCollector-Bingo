# Emote Collector Bingo
Created for the Emote Moderators of Emote Collector.

- `python -m ec_bingo new`
- `python -m ec_bingo mark <point> <name> < board.json > new-board.json`
  (To overwrite board.json in place, use the `sponge` command from moreutils.)
- `python -m ec_bingo unmark <point> < board.json > new-board.json`
- `python -m ec_bingo render < board.json > board.png`

Creates a new bingo board for use with Emote Collector,
or marks a point on an existing board.

## Commands

### ec_bingo new
Generates a new board. Outputs the new board data (as JSON) to stdout.

### ec_bingo mark <point\> <emote name\>
Marks a point on the board. Use a letter of `BINGO` + a number
as a marker for this point, e.g. `mark B3 Steve1`.
`N3` is invalid. Reads the current board data from stdin, writes the new board data to stdout.

### ec_bingo unmark <point\>
Unmarks a point on the board.

### ec_bingo render
Reads board data from stdin and renders it as a PNG image to stdout.

## License

Copyright © 2019 Xua, Io Mintz \
All Rights Reserved.

This project is provided under the BlueOak Model License 1.0.0. See LICENSE.md for details.

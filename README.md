# Emote Collector Bingo
Created for the Emote Moderators of Emote Collector.

`python -m ec_bingo new`
`python -m ec_bingo mark <point> <name>`
`python -m ec_bingo render < board.json > board.png`

Creates a new bingo board for use with Emote Collector,
or marks a point on an existing board.

## ec_bingo new
Generates a new board for use. Outputs the new board data (as JSON) to stdout.

## ec_bingo mark <point\> <emote name\>
Marks a point on the board. Use a letter of `BINGO` + a number
as a marker for this point, e.g. `mark B3 Steve1`.
`N3` is invalid. Reads the current board data from stdin, writes the new board data to stdout.

## ec_bingo render
Reads board data from stdin and renders it as a PNG image to stdout.

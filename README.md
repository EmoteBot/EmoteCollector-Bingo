# Emote Collector Bingo
Created for the Emote Moderators of Emote Collector.

`python -m ec_bingo <new|mark <point> <name>>`

Creates a new bingo board for use with Emote Collector,
or marks a point on an existing board.

## ec_bingo new
Generates a new board for use. Outputs the new board to stdout.

## ec_bingo mark <point\> <emote name\>
Marks a point on the board. Use a letter of `BINGO` + a number
as a marker for this point, e.g. `mark b3 Steve1`.
`n3` is invalid. Reads the current board from stdin, writes the new board to stdout.


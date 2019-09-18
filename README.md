# Emote Collector Bingo
Created for the Emote Moderators of Emote Collector.

`python -m ec_bingo <new|mark <point> <name>>`

Creates a new bingo board for use with Emote Collector,
or marks a point on an existing board.

Or, marks a point on an existing board.
You can specify a path under the env var ECBINGOBOARD
or if left unset, searches for one in the current working
directory.

#### ec_bingo new
Generates a new board for use.

#### ec_bingo mark <point\> <emote name\>
Marks a point on the board. Use a letter of `BINGO` + a number
as a marker for this point, e.g. `mark b3 Steve1`.
`n3` is invalid.
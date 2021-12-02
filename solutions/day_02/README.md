# Overview of Problem
## Part 1
Part 1 was to parse three different types of commands:
`forward [number]`
`up [number]`
and `down [number]`, where up would decrease the depth by number, down would increase the depth by number,
and forward would increase the horizontal value by number. At the end, you multiply depth by the horizontal value.
## Part 2
Part 2 was to use the same commands but add an aim feature where aim replaced
depth except depth was now increased by aim * the current horizontal value for when forward is called.
Then, at the end, you multiply depth by the horizontal value to get your result!

# My Thought Process
## Part 1
I decided to use `match`/`case`, new Python features, which allowed pattern matching to parse the commands and calculate it out.
## Part 2
Part 2 had the same implementation as Part 1, except adding a depth variable that increased in `case (forward, num):`
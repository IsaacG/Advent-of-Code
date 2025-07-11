# Marches & Gnats

> Marches & Gnats is a fantastical game of programming challenges set in 19th-century Estonia, where each challenge is both a story and a test of your computational ingenuity. Craft precise instructions for the Logic Mill—a secret mechanical Turing machine—and help Mihkel, a quiet genius of Dorpat, turn the hidden order of the world into working code.

Website: [mng.quest](https://mng.quest/)

## Description

This challenge asks you to solve eight (8) puzzles by writing a "Turing machine program", a set of state transitions.
Each program consists of one or more lines.
Each line has a match clause (the current state and current symbol under the head), the output clause (new state and new symbol to write under the head) as well as a move direction (L, R).
`CURRENT_STATE CURRENT_SYMBOL NEW_STATE NEW_SYMBOL DIRECTION`.

## My solutions

For the first six (6) quests, I hand wrote the programs.
The longest is 21 lines.
The last two (2) quests, quests 7 and 8, need to handle 31 unique characters.
This gives rise to a large number of states (on the order of 31x31) -- much to many to hand write.
Instead, I wrote some Python code to generate the program for those quests.

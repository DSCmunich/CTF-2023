# GDSC TUM 2023 - "Boring Maze" (pwn)

SPOILER ALERT: please don't read this if you intend to beta-test the chall

## Overview

- ELF x86_64 LSB, PIE, NX, canaries, ASLR enabled. Running on a Linux system (ex: a Debian docker)
- looks like a maze solving chall, as can be seen in many CTFs. Maze size is N = 16, 32 or 64 (to be determined, depending on the difficulty we want to have), but reaching the "treasure" won't give the flag, it just prints a congrats message and ask you to REALLY escape the maze (one has to actually pwn the program to get a shell from it)
- maze statically generated and hard coded in the binary (same maze at every run)
- spawn at one corner of the maze, "treasure" (`$`) at the opposite corner, walls (`#`) all around the maze. Even if somehow you manage to get to the edge of the maze despite the walls, you are not allowed to move past its boundaries
- move with `WASD`, can take multiple commands on one line (ex: send "WWWDDSA\n", it will move you around, tell you if you die on the way, and else show your new position and surroundings after)
- local view only : one can only see what's in a 3*3 rectangle around them (distance of 1)
- the treasure is actually circled by walls and can't be reached
- somewhere in the maze there is a genius/mage/magic scroll/whatever (`!`) that can be met only once (disappears after) and grants you one superpower among:
    - "vision": increases the local view range by one (becomes a 5*5 rectangle, distance of 2)
    - "wall": allows to create a wall in front of you with `M`
    - "teleport": teleport anywhere in the maze, but it is denied to you if you ask for it

## Vulns

- "vision" allows out-ouf bounds read: if you are next to a wall, you can see outside the maze
- "wall" is implemented by adding `3` (`'#' - ' '`) to the tile in front of you, but if you use it several times, you can add `3` an arbitrary number of time to the tile, and thus have arbitrary write in front of you because `3` is relatively prime with `256`. You can thus destroy walls, turn any wall into the treasure or into the genius
- "vision" is implemented by adding `1` to a global variable that tells how far you can see -> can be incremented several times if you manage to call the genius several times -> can thus reach arbitrary values
- the vision range, a boolean telling whether you can teleport and one telling whether you can build walls are stored as global variables just before the maze

## exploit 

- use the previously mentioned vulns to give you a large vision range: you can get a very large vision range either by calling the genius many times (but that's long), or by noticing that there is one value near the maze that increases by one every time you increase your vision -> break the wall next to it, then use the maze building power to make it arbitrarily high
- use the wall power to allow yourself to teleport-> you now have arbitrary read and write
- exploit by overwriting the GOT


# Ez Pwn

While still a classic buffer overflow challenge with win function, we now take things
a tiny bit further. The technique of bluntly overwriting the return address is now
prevented by a stack canary: This random value sits just before the return address on
the stack and thus will be destroyed by any buffer overflow that tries to reach the
return address. Before returning, the program will first check if the canary is still
intact, and if this is not the case, it will terminate immediately, to prevent attackers
from assuming control.

Of course, nothing is hacker-proof and this can also be circumvented: In this program
we are not only able to write into a buffer, but also read from it. This is very
convenient, since we can just let the program read its "secret" canary value back to us,
so that we can adapt our buffer overflow to not only overwrite the return address but
also restore the canary value while doing so.

First, we overflow buf by sending exactly the amount of bytes that is needed from buf
start to the canary, e.g. filling this space with lots of "A"s. Note that the canary
deliberately starts with a zero-byte to "prevent" what we will be doing next, but we
can just overwrite this with an "A" for now as well.

If we then request the program to read the data back to us, this will be done by
treating buf as a regular zero-terminated string. This means, that of course
everything from buf start to the first following zero byte will be printed, which will
be all our "A"s AND the (last 7 bytes of the) canary!

Since we get multiple rounds of commands, we can now again request to write to buf,
again filling the space until the start of the canary, adding the expected single
zero byte, the rest of the canary and then continue to overwrite the return address
with the win function as usual.

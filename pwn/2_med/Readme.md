# Medium Pwn

Now that we know how to exploit classical buffer overflows, even with a stack canary,
it's time to introduce a new way of executing arbitrary code after being able to
overwrite the return address: Return Oriented Programming (ROP)

As we see, there is no (sensible) win function this time, so overwriting the return
address with a single new address is not the way to victory this time. Taking a look
around the program shows us that it prints the address of the printf function, which
may seem odd to people that are new to pwn challenges, but there is of course a reason
for this:

ROP is a technique that takes advantage of existing code fragments called "gadgets" to
let the program execute precisely the code the attacker wants. Imagine a puzzle where
you can only use pieces from a pre-existing set to build something new. Similarly, ROP
takes short snippets of code already present in a program's memory to assemble a
sequence of actions. These gadgets typically end with a "return" instruction, hence the
name "return-oriented" programming.

ROP is actually Turing-complete by the way, so you can really run any code you like with
it, but for this to be possible, the existing program needs to be sufficiently large.
This is the issue in our case: Even if we were to re-use pieces of the vuln binary,
we wouldn't be able to execute code to open a shell for us. This is where the printf
address comes into play: If we know where printf was loaded to during runtime, we also
know where the full libc (the C standard library that has all the functions like printf)
is located. The libc naturally is a massive piece of code, since it needs to provide all the
important standard library functions, so from a ROP perspective, it also meets this
criterion of being "sufficiently large", allowing us to execute all the gadgets we need,
as soon as we know its address in memory.

What we can do now is as follows: We want to execute the libc function "system" and
pass "/bin/sh" as the argument, which will lead to a new shell being opened. The first
argument to any function is passed via the RDI register on x64, so at the time when we
execute "system", RDI will need to contain a pointer to the "/bin/sh" string. Luckily
for us, libc itself already contains this string, so we can just check at what offset
it is (e.g. using `libc.search(b"/bin/sh")` in pwntools).

Now the first task of our ROP chain will be to store this address in RDI. We can do
this using a gadget that executes `pop rdi` followed by `ret` (The address of such
gadgets can be found using tools like `ropper`:
`ropper -f libc.so --search "pop rdi; ret;"`). Recall that we are able to overflow a
buffer on the stack, so we control everything that's on it for as long as we like.
If we place the address of this gadget on the location of the return address, what will
happen is that the program will "return" to the `pop rdi` instruction, which stores
the next value on the stack (which we also control! it's just the next 8-byte value)
after the return address we just overwrote) in RDI.

After RDI has been initialized correctly, we can execute `system`: Since our gadget not
only executes `pop rdi` but also follows this by a `ret` instruction, it will look up
the next value on the stack (again, something we control) and "return" to this address.
If we conveniently just place the address of `system` here, the program will execute it
as if it was called with `system("/bin/sh")`. Anything we send to the program now will
be piped to a newly opened shell, and we can simply execute `get_flag` and read the flag.

But what's this? Seems like the program doesn't open a shell after all and just crashes?!
This is a bit of a nasty situation that has the potential to cost you some time if you
don't look closely, but what happens is that `system` is indeed executed correctly, but
somewhere down the line while it tries to open the shell it uses x64 vector instructions.
Why they are used is not relevant, it's doing some string manipulation, but ultimately
the important part here is that whenever such an instruction is to be executed, the
stack address in RSP needs to be aligned to 16 bytes (i.e. end on a 0). If you just
perform the ROP chain as we discussed it above, RSP will end in an 8 instead of a 0
when it reaches the first vector instruction, leading to a crash. Luckily we can fix
this: Before we execute the `pop rdi; ret;` gadget, we execute another gadget, this
time simply `ret;`. This is equivalent to a `nop` in ROP terms, but has the effect
that the rest of the stack that comes after this gadget's address is shifted down by
one address (i.e. 8 bytes), leading to the desired 16 byte alignment inside `system`.
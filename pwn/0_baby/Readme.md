# Baby Pwn

This is an all-time classic: A program reads user input into a buffer that has fixed size,
but lets the user control how many bytes are being read. This is of course not a good idea,
since if you tell the program it will receive a message of 500 bytes for example, it will
gladly read it into its tiny 42 bytes buffer, completely spilling the received data across
buffer boundaries onto the rest of the stack, including the return address.

Thus, you take a look in a debugger how far away the return address is from the buffer start
and insert a new value at this place by sending an appropriate amount of garbage bytes
before. Since the program in this particular case has a "win function" that takes care
of executing "/bin/get_flag", we can use its address here and have the program execute it
after it finished the main function.
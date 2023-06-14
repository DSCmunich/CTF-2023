CC=gcc
CFLAGS=-Wall -ggdb -fno-stack-protector -z execstack -no-pie -Wl,-z,norelro

default: all

all: vuln

vuln: vuln.c
	$(CC) $(CFLAGS) -o vuln vuln.c

clean:
	rm -f vuln

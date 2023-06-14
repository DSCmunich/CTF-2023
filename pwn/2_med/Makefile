CC=gcc
CFLAGS=-Wall -ggdb -fno-stack-protector

default: all

all: vuln

vuln: vuln.c
	$(CC) $(CFLAGS) -o vuln vuln.c

clean:
	rm -f vuln

CC=gcc
CFLAGS=-Wall -ggdb -no-pie

default: all

all: vuln

vuln: vuln.c
	$(CC) $(CFLAGS) -o vuln vuln.c

clean:
	rm -f vuln

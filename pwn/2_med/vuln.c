#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win() {
    // TODO Don't forget to finish coding the win function before the CTF starts!
    exit(1);
}

int main() {
    // Set stdout and stdin to be unbuffered to avoid communication issues over the network
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stdin, 0, _IONBF, 0);

    printf("I would love to know your favorite number! I'll go first, mine is %p!\n", printf);
    printf("How many digits does your favorite number have (max: 10)?\n");
    char buf[30] = { 0 }; // 3x the size should be a good hacker protection!
    fgets(buf, sizeof(buf) - 1, stdin);
    long int length = strtoul(buf, NULL, 0);
    if (length > 10) {
        printf("Ha! Did you think you could trick me?!\n");
        exit(1);
    }

    printf("Please send your number now:\n");
    fgets(buf, length, stdin);
    printf("%#llx indeed is a great number, good choice!\n", strtoull(buf, NULL, 0));

    return 0;
}

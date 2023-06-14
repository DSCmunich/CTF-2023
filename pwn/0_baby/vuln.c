#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win() {
    execl("/bin/get_flag", NULL, NULL);
    exit(1);
}

int main() {
    // Set stdout and stdin to be unbuffered to avoid communication issues over the network
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stdin, 0, _IONBF, 0);

    char buf[42];
    printf("Welcome to the PWN category of GDSC Munich CTF 2023!\n"
           "Before we start, we'd like to get to know you a bit better, "
           "so please tell us something about yourself. How many characters "
           "will your message have?\n");
    read(STDIN_FILENO, buf, sizeof(buf) - 1);
    int msgSize = atoi(buf);

    printf("Please send us your message now (%d characters):\n", msgSize);
    read(STDIN_FILENO, buf, msgSize);
    printf("Thank you, your response has been stored in our system!\n\n"
           "User 12753's message: %s\n", buf);
    return 0;
}

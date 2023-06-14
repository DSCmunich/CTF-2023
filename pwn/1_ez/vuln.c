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

    char quote[] = "Try spinning, that's a good trick!";
    while (1) {
        printf("Easy times are over, so to help you through the tough challenges "
               "that are coming up next, we provide you with some extra motivational quotes.\n"
               "These are your options:\n"
               "1: Read motivational quote\n"
               "2: Send your own motivational quote\n"
               "Anything else: Exit\n");
        char buf[10] = { 0 };
        read(STDIN_FILENO, buf, sizeof(buf) - 1);
        int option = atoi(buf);

        switch (option) {
            case 1:
                puts(quote);
                break;
            case 2:
                printf("How long is your quote?\n");
                read(STDIN_FILENO, buf, sizeof(buf) - 1);
                int len = atoi(buf);
                printf("Please send your quote now (%d characters):\n", len);
                read(STDIN_FILENO, quote, len);
                break;
            default:
                printf("Good bye\n");
                return 0;
        }
        puts("");
    }


    return 0;
}

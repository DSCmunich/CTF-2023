#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

#define N 65
#define NAME_LEN 32

#define ALARM_SECONDS 300

enum card {NORTH, SOUTH, EAST, WEST};

enum card dir;
int x, y;
int view_range;
int can_teleport;
int can_wall;
char maze[N][N];
char player_name[NAME_LEN];

void init_maze() {
    alarm(ALARM_SECONDS);
    setvbuf(stdout, (char *)0x0, 2, 1);
    x = 1;
    y = 1;
    dir = EAST;
    view_range = 1;
    can_teleport = 0;
    can_wall = 0;
    int fd = open("./maze.txt", O_RDONLY);
    read(fd, maze, N*N);
    close(fd);
}

void view() {
    for (int i = x - view_range; i <=  x + view_range; i++) {
        for (int j = y - view_range; j <= y + view_range; j++) {
            putchar(maze[i][j]);
        }
        putchar('\n');
    }
}

void mage() {
    char c = 0;
    while (c != '\n') {
        c = getchar();
        if (c == EOF) {
            exit(EXIT_FAILURE);
        }
    }
    puts("OHOHOHOHOHOHO hello, I am the omnipotent mage, and this maze is about to become much more exciting!");
    puts("I will grant you one superpower among: ");
    puts("- (V) vision: allows you to see further");
    puts("- (M) mason: allows you to build a wall in front of you");
    puts("- (T) teleport: allows you to teleport anywhere in and out of the maze");
    puts("Which one do you want?");
    c = getchar();
    switch (c)
    {
    case EOF:
        exit(EXIT_FAILURE);
        break;
    case 'V':
        view_range += 1;
        puts("Wow, no need to wear glasses anymore!");
        break;
    case 'M':
        can_wall = 1;
        puts("Woosh, you can now build a wall in front of you with 'M', and get even more stuck!");
        break;
    case 'T':
        puts("Haha no way, that would be to easy!");
        break;
    default:
        puts("Huuuum I said 'V', 'M', or 'T', seems like some people are just too dumb to receive superpowers");
        break;
    }
    while (c != '\n') {
        c = getchar();
        if (c == EOF) {
            exit(EXIT_FAILURE);
        }
    }
    puts("Now I have to teleport away, bye!");
    maze[x][y] = ' ';
    view();
}

void get_facing(int *fx, int *fy) {
    switch (dir)
    {
    case NORTH:
        *fx = x - 1;
        *fy = y;
        break;
    case SOUTH:
        *fx = x + 1;
        *fy = y;
        break;
    case EAST:
        *fx = x;
        *fy = y + 1;
        break;
    case WEST:
        *fx = x;
        *fy = y - 1;
        break;
    default:
        fprintf(stderr, "Current dir is invalid: %d\n", dir);
        exit(EXIT_FAILURE);
        break;
    }
}

void flipdir() {
    switch (dir)
    {
    case NORTH:
        dir = SOUTH;
        break;
    case SOUTH:
        dir = NORTH;
        break;
    case EAST:
        dir = WEST;
        break;
    case WEST:
        dir = EAST;
        break;
    default:
        fprintf(stderr, "Current dir is invalid: %d\n", dir);
        exit(EXIT_FAILURE);
        break;
    }
}

void turn_right() {
    switch (dir)
    {
    case NORTH:
        dir = EAST;
        break;
    case SOUTH:
        dir = WEST;
        break;
    case EAST:
        dir = SOUTH;
        break;
    case WEST:
        dir = NORTH;
        break;
    default:
        fprintf(stderr, "Current dir is invalid: %d\n", dir);
        exit(EXIT_FAILURE);
        break;
    }
}

void turn_left() {
    switch (dir)
    {
    case NORTH:
        dir = WEST;
        break;
    case SOUTH:
        dir = EAST;
        break;
    case EAST:
        dir = NORTH;
        break;
    case WEST:
        dir = SOUTH;
        break;
    default:
        fprintf(stderr, "Current dir is invalid: %d\n", dir);
        exit(EXIT_FAILURE);
        break;
    }
}

void handle_move(char c) {
    switch (c)
    {
    case 'W':
        break;
    case 'A':
        turn_left();
        break;
    case 'S':
        flipdir();
        break;
    case 'D':
        turn_right();
        break;
    default:
        fprintf(stderr, "Illegal move: %c\n", c);
        exit(EXIT_FAILURE);
        break;
    }
    int newx, newy;
    get_facing(&newx, &newy);
    if (newx < 0 || newy < 0 || newx >= N || newy >= N) {
        fputs("Can't escape the maze!\n", stderr);
        exit(EXIT_FAILURE);
    }
    x = newx;
    y = newy;
    switch (maze[x][y])
    {
    case '#':
        fputs("Wall. You die.\n", stderr);
        exit(EXIT_FAILURE);
        break;
    case '$':
        puts("Treasure!");
        puts("... empty ...");
        puts("All this for nothing.");
        puts("*digs own grave*");
        puts("---------");
        puts("R.I.P");
        puts(player_name);
        puts("unknown - 30th of June 2023");
        puts("---------");
        exit(EXIT_FAILURE);
        break;
    case '!':
        mage();
        break;
    default:
        break;
    }
}

int main(int argc, char const *argv[])
{
    char c;
    init_maze();
    puts("Welcome. Boring maze.");
    puts("Player name:");
    fgets(player_name, NAME_LEN, stdin);
    for (int i = 0; i < N; i++) {
        if (player_name[i] == '\n') {
            player_name[i] = 0;
        }
    }
    puts("Move: WASD. Can give several in a row.");
    printf("%s: (%d, %d), facing East\n", player_name, x, y);
    printf("Treasure: (%d, %d)\n", N - 1, N - 1);
    view();

    while(1) {
        c = getchar();
        switch (c)
        {
        case EOF:
            exit(EXIT_FAILURE);
            break;
        case '\n':
            view();
            break;
        case 'W':
        case 'A':
        case 'S':
        case 'D':
            handle_move(c);
            break;
        case 'T':
            if (can_teleport) {
                //why would I bother doing proper input reading and checking if the user can't teleport anyway ?
                fread(&x, 1, sizeof(x), stdin);
                fread(&y, 1, sizeof(y), stdin);
            }
            else {
                fprintf(stderr, "Unknown command: %c\n", c);
            }
            break;
        case 'M':
            if (can_wall) {
                int fx, fy;
                get_facing(&fx, &fy);
                maze[fx][fy] += '#' - ' ';
            }
            else {
                fprintf(stderr, "Unknown command: %c\n", c);
            }
            break;
        default:
            fprintf(stderr, "Unknown command: %c\n", c);
            break;
        }
    }
    return 0;
}

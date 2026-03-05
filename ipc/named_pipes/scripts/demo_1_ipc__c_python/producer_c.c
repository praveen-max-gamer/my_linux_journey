#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>

int main()
{
    const char *named_pipe = "demo_pipe_1";
    int fd = open(named_pipe, O_WRONLY);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    const char *msg = "Hello Python\n";
    printf("C - Producer writing to named pipe : %s\n",named_pipe);
    while (1) {
        write(fd, msg, 13);
        usleep(100000); // 0.1 seconds (ms)a
    }

    close(fd);
    return 0;
}

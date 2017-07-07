#include <stdio.h>
#include <stdlib.h>

struct Address
{
    int id;
    char *name;
    char *email;
};


int main(int argc, char const *argv[])
{
    struct Address *addr = malloc(sizeof(struct Address));
    addr->id = 1;
    addr->name = "ekeyme";
    addr->email = "ekeyme@gmail.com";

    printf("The email of %s: %s: %d\n", addr->name, addr->email, addr->id);
    free(addr);
    return 0;
}

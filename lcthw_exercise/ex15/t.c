#include <stdio.h>

int main(int argc, char *argv[])
{
    char *names[] = {
        "Alan", "Frank",
        "Mary", "John", "Lisa"
    };

    int i = 0;
    for (i = 0; i < 5; i++){
        printf("%p, %s\n", *&names[i], *&names[i]);
    }

    for (i = 0; i < 5; i++) {
        printf("value: %s, address: %p, address2: %p, address2 int: %p\n", *(names + i), names + i, *(names + i), &(*(names + i)));
    }

    return 0;
}

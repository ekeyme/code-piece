#include <stdio.h>

char toLowerCase(char letter)
{
    if (letter >= 65 && letter <=90) {
        return letter + 32;
    } else {
        return letter;
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("ERROR: You need one argument.\n");
        
        // this is how you abort a program
        return 1;
    }

    int i = 0;
    for (i = 0; argv[1][i] != '\0'; i++) {
        char letter = argv[1][i];
        char lowerCaseLetter = toLowerCase(letter);

        switch (lowerCaseLetter) {
            case 'a':
                printf("%d: '%c'\n", i, letter);
                break;
            case 'e':
                printf("%d: '%c'\n", i, letter);
                break;
            case 'i':
                printf("%d: '%c'\n", i, letter);
                break;
            case 'o':
                printf("%d: '%c'\n", i, letter);
                break;
            case 'u':
                printf("%d: '%c'\n", i, letter);
                break;
            case 'y':
                if (i > 2) {
                    // it's only sometimes Y
                    printf("%d: '%c'\n", i, letter);
                }
                break;
            default:
                printf("%d: %c is not a vowel\n", i, letter);
                break;
        }
    }

    return 0;
}

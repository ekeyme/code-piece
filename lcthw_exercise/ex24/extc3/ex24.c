#include <stdio.h>
#include <ctype.h>
#include "dbg.h"

#define MAX_DATA 100

typedef enum EyeColor {
    BLUE_EYES, GREEN_EYES, BROWN_EYES,
    BLACK_EYES, OTHER_EYES
} EyeColor;

const char *EYE_COLOR_NAMES[] = {
    "Blue", "Green", "Brown", "Black", "Other"
};

typedef struct Person {
    int age;
    char first_name[MAX_DATA];
    char last_name[MAX_DATA];
    EyeColor eyes;
    float income;
} Person;

// Trims leading whitespace chars in left `str`, then copy at almost `n - 1` chars
// into the `out` buffer in which copying might stop when the first '\0' occurs, 
// and finally append '\0' to the position of the last non-trailing whitespace char.
// Reture the length the trimed string which '\0' is not count in like strlen().
size_t trim(char *out, size_t n, const char *str)
{
    // do nothing
    if(n == 0) return 0;

    // ptr stop at the first non-leading space char
    while(isspace(*str)) str++;

    if(*str == '\0') {
        out[0] = '\0';
        return 0;
    }

    size_t i = 0;

    // copy char to out until '\0' or i == n - 1
    for(i = 0; i < n - 1 && *str != '\0'; i++){
        out[i] = *str++;
    }

    // deal with the trailing space
    while(isspace(out[--i]));

    out[++i] = '\0';
    return i;
}

int main(int argc, char *argv[])
{
    Person you = {.age = 0 };
    int i = 0;
    int rc = 0;
    char buffer[MAX_DATA];
    char *in = NULL;

    printf("What's your First Name? ");
    in = fgets(buffer, MAX_DATA, stdin);
    check(in != NULL, "Failed to read first name.");
    rc = trim(you.first_name, MAX_DATA, buffer);
    check(rc > 0, "missing first name.")

    printf("What's your Last Name? ");
    in = fgets(buffer, MAX_DATA, stdin);
    check(in != NULL, "Failed to read last name.");
    rc = trim(you.last_name, MAX_DATA, buffer);
    check(rc > 0, "missing last name.")

    printf("How old are you? ");
    rc = fscanf(stdin, "%d", &you.age);
    check(rc > 0, "You have to enter a number.");

    printf("What color are your eyes:\n");
    for (i = 0; i <= OTHER_EYES; i++) {
        printf("%d) %s\n", i + 1, EYE_COLOR_NAMES[i]);
    }
    printf("> ");

    int eyes = -1;
    rc = fscanf(stdin, "%d", &eyes);
    check(rc > 0, "You have to enter a number.");

    you.eyes = eyes - 1;
    check(you.eyes <= OTHER_EYES
            && you.eyes >= 0, "Do it right, that's not an option.");

    printf("How much do you make an hour? ");
    rc = fscanf(stdin, "%f", &you.income);
    check(rc > 0, "Enter a floating point number.");

    printf("----- RESULTS -----\n");

    printf("First Name: %s\n", you.first_name);
    printf("Last Name: %s\n", you.last_name);
    printf("Age: %d\n", you.age);
    printf("Eyes: %s\n", EYE_COLOR_NAMES[you.eyes]);
    printf("Income: %f\n", you.income);

    return 0;
error:

    return -1;
}

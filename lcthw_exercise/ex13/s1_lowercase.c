#include <stdio.h>

int main(int argc, char *argv[])
{
	if (argc != 2){
		printf("error: you need one argument.\n");
	}

	int i = 0;
	for (i = 0; argv[1][i] != '\0'; i++){
		char letter = argv[1][i];
		if (97 <= letter && letter <= 122){
			letter = letter - 32;
		}

		switch (letter){
			case 'A':
			case 'B':
			case 'C':
			case 'D':
			case 'E':
			case 'F':
			case 'G':
			case 'H':
			case 'I':
			case 'J':
			case 'K':
			case 'L':
			case 'M':
			case 'N':
			case 'O':
			case 'P':
			case 'Q':
			case 'R':
			case 'S':
			case 'T':
			case 'U':
			case 'V':
			case 'W':
			case 'X':
			case 'Y':
			case 'Z':
				printf("%c", letter);
				break;

			default:
				break;
		}
	}

	printf("\n");

	return 0;
}

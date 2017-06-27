#include <stdio.h>

int main(int argc, char *argv[])
{
	// go through each string in argv

	int i = 0;
	while(i < argc) {
		printf("arg %d: %s\n", i, argv[i]);
		i++;
	}

	// sign argv to states
	char *states[9999] = {'\0'};

	i = 0;
	while(i < argc) {
		states[i] = argv[i];
		i++;
	}

	// go through each string in states
	i = 0;
	while (i < argc){
		printf("states %d: %s\n", i, argv[i]);
		i++;
	}

	return 0;
}

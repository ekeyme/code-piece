#include <stdio.h>

int main(int argc, char const *argv[])
{
	int i = 0;

	// go througn each string in argv
	// why am I skipping argv[0]
	for (i=1; i<argc; i++){
		printf("arg %d: %s\n", i, argv[i]);
	}

	// let's make our own array of stings
	char *states[] = {
		"California", "Oregon",
		"Washington", "Texas"
	};
	int num_status = 6;

	for (i=0; i<num_status; i++){
		printf("states %d: %s\n", i, states[i]);
	}

	return 0;
}
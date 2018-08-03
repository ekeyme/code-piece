#include <stdio.h>

int main(int argc, char *argv[])
{

	if (argv[1] == "-h" || argv[1] == "--help"){
		printf("usage: ....\n");
	}else{
		printf("APP run.\n");
	}

	return 0;
}

#include <stdio.h>

// convert 4-byte char into int
int main(int argc, char *argv[])
{
	char name[] = {'Z', 'e', 'd', '\0'};
	int i;

	printf("%s\n", name);

	i = (name[0]<<24) + (name[1]<<16) + (name[2]<<8) + name[3];
	printf("%x\n", i);
	printf("%d\n", i);

	return 0;
}
#include <stdio.h>

// convert 4-byte char into int
int main(int argc, char const *argv[])
{
	char *another = "Zed";
	int i;

	printf("%s\n", another);

	i = (another[0]<<24) + (another[1]<<16) + (another[2]<<8) + another[3];
	printf("%x\n", i);
	printf("%d\n", i);

	return 0;
}
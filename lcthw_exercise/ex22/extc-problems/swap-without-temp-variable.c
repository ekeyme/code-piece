#include<stdio.h>

int main()
{
	int val1 = 10;
	int val2 = 50;
	printf("val1: %d, val1 address: %p; val2: %d, val2 address: %p\n", val1, &val1, val2, &val2);
	// swap them using pointer
	val1^=val2;
	val2^=val1;
	val1^=val2;
	printf("val1: %d, val1 address: %p; val2: %d, val2 address: %p\n", val1, &val1, val2, &val2);

	return 0;
}
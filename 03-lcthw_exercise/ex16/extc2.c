#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>

struct Person {
	char *name;
	int age;
	int height;
	int weight;
};


// this shows how to initialize a struct using the x.y (period) characher instead of the x->y syntax.
int main(int argc, char *argv[])
{
	struct Person who = {.name="ekeyme", .age=18, .height=180, .weight=80};
	
	printf("Name: %s\n", who.name);
	printf("\tAge: %d\n", who.age);
	printf("\tHeight: %d\n", who.height);
	printf("\tWeight: %d\n", who.weight);

	return 0;
}

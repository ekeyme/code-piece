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

int main(int argc, char *argv[])
{
	struct Person who = {"ekeyme", 18, 180, 80};
	struct Person *cur_who = &who;

	printf("%d\n", (*cur_who).age);

	printf("Name: %s\n", who.name);
	printf("\tAge: %d\n", who.age);
	printf("\tHeight: %d\n", who.height);
	printf("\tWeight: %d\n", who.weight);

	return 0;
}

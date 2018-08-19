#include <stdio.h>

struct Person{
	char *name;
	int age;
	int height;
	int weight;
};

struct Person Person_create(char *name, int age, int height, int weight)
{
	struct Person who = {.name=name, .age=age, .height=height, .weight=weight};

	return who;
}

void Person_print(struct Person who)
{
	printf("Name: %s\n", who.name);
	printf("\tAge: %d\n", who.age);
	printf("\tHeight: %d\n", who.height);
	printf("\tWeight: %d\n", who.weight);
}

// this shows how to pass a structure to other functions without using a pointer.
int main(int argc, char *argv[])
{
	// make two people structures
	struct Person joe = Person_create("joe Alex", 32, 64, 140);

	struct Person frank = Person_create("Frank Blank", 20, 72, 180);

	// print them out and where they are in memory
	printf("Joe is at memory location %p:\n", (void*)&joe);
	Person_print(joe);

	printf("Frank is at memory location %p:\n", (void*)&frank);
	Person_print(frank);

	// make everyone age 20 years and print them agin
	joe.age += 20;
	frank.age += 20;

	Person_print(joe);
	Person_print(frank);

	return 0;
}

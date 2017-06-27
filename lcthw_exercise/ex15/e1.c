#include <stdio.h>

int main(int argc, char *argv[])
{
	// create two array we care about
	int ages[] = {23, 43, 12, 89, 2};
	char *names[] = {
		"Alan", "Frank", 
		"Marry", "John", "Lisa"
	};

	// safely get the size of ages
	int count = sizeof(ages) / sizeof(int);
	int i = 0;

	// first way using indexing
	for (i = 0; i < count; i++){
		printf("%s has %d years alive.\n", names[i], ages[i]);
	}

	printf("---\n");

	// first cast the pointer array, names, which contains the pointers pointing to strings(char*), into pointer of the array, then signed it to cur_age. That asume the elements in the cur_age are long int type, but in fact, these long int are pointers(address) piointing to strings(char*).
	long *cur_age = (long*)names;
	char **cur_name = names;

	// second way using pointers
	for (i = 0; i < count; i++){
		// in here `(char *) *(cur_age+i)`: *(cur_age+i) get the value(long int) from cur_age, then, `(char *)` cast it into a pointer pointing an array of char(char[]), that is string. Finally the `%s` of printf konw how to do the left things, it first find the address the pointer indicating, then start to concatenate the char until '\0' in subsequence address of memmory, and the print them out. 
		printf("%s is %s years old.\n", *(cur_name+i), (char *) *(cur_age+i));
	}

	return 0;

}

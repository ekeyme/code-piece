#include <stdio.h>
#include "dbg.h"

#define COUNT 100000000


int valid_copy(char *data, int count, char expects)
{
	int i = 0;
	for(i = 0; i < count; i++) {
		if(data[i] != expects) {
			log_err("[%d] %c != %c", i, data[i], expects);
			return 0;
		}
	}

	return 1;
}

int main(int argc, char const *argv[])
{
	char to[1000] = {'a'};
	char from[1000] = {'x'};
	// set from to 1000 'b'
	memset(from, 'b', 1000);
	check(valid_copy(from, 1000, 'b'), "from initial failed");

	// test memcpy
	void *rc = memcpy(to, from, 1000);
	check(rc == to, "memcpy copy failed");
	check(valid_copy(to, 1000, 'b'), "memcpy copy failed");
	timeit(memcpy(to, from, 1000), COUNT);

	// fast reset
	to[0] = '\0';

	// test memmove
	rc = memmove(to, from, 1000);
	check(rc == to, "memmove copy failed");
	check(valid_copy(to, 1000, 'b'), "memmove copy failed");
	timeit(memmove(to, from, 1000), COUNT);

	to[0] = '\0';
	// test memset
	memset(to, 'b', 1000);
	check(valid_copy(to, 1000, 'b'), "memset failed");
	timeit(memset(to, 'b', 1000), COUNT);

	return 0;
error:
	return 1;
}
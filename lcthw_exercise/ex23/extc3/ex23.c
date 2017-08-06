#include <stdio.h>
#include <string.h>
#include "dbg.h"


// define simple case expression macro
#define case_1(...) case 1: __VA_ARGS__
#define case_2(...) case 2: __VA_ARGS__;\
					case_1(__VA_ARGS__)
#define case_3(...) case 3: __VA_ARGS__;\
					case_2(__VA_ARGS__)
#define case_4(...) case 4: __VA_ARGS__;\
					case_3(__VA_ARGS__)
#define case_5(...) case 5: __VA_ARGS__;\
					case_4(__VA_ARGS__)
#define case_6(...) case 6: __VA_ARGS__;\
					case_5(__VA_ARGS__)
#define case_7(...) case 7: __VA_ARGS__;\
					case_6(__VA_ARGS__)
#define case_8(...) case 8: __VA_ARGS__;\
					case_7(__VA_ARGS__)
#define ncase(N, ...) case_##N(__VA_ARGS__)


int normal_copy(char *from, char *to, int count)
{
	int i = 0;

	for(i = 0; i < count; i++) {
		to[i] = from[i];
	}

	return i;
}

int duffs_device(char *from, char *to, int count)
{
	{
		int n = (count + 7) / 8;

		switch(count % 8) {
			case 0:
				do {
					*to++ = *from++;
					ncase(7, *to++ = *from++);
				} while(--n > 0);
		}
	}

	return count;
}

int zeds_device(char *from, char *to, int count)
{
	{
		int n = (count + 7) / 8;

		switch(count % 8) {
			case 0:
again:		*to++ = *from++;
			
			ncase(7, *to++ = *from++);
			if(--n > 0) goto again;
		}
	}

	return count;
}

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
	char from[1000] = {'a'};
	char to[1000] = {'c'};
	int rc = 0;

	// setup the from to have some stuff
	memset(from, 'x', 1000);
	// se it to a failure mode
	memset(to, 'y', 1000);
	check(valid_copy(to, 1000, 'y'), "Not initialized right.");

	// use normal copy to
	rc = normal_copy(from, to, 1000);
	check(rc == 1000, "Normal copy failed: %d", rc);
	check(valid_copy(to, 1000, 'x'), "Normal copy failed.");

	//reset
	memset(to, 'y', 1000);

	// duffs version
	rc = duffs_device(from, to, 1000);
	check(rc == 1000, "Duff's device failed: %d", rc);
	check(valid_copy(to, 1000, 'x'), "Duff's device failed copy.");

	// reset
	memset(to, 'y', 1000);

	// my version
	rc = zeds_device(from, to, 1000);
	check(rc == 1000, "Zed's device failed: %d", rc);
	check(valid_copy(to, 1000, 'x'), "Zed's device failed copy.");

	return 0;

error:
	return 1;
}

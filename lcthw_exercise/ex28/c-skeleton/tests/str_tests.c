#include "str.h"
#include "dbg.h"
#include <string.h>

int main()
{
	char *s = "abc123";
	char *ex = "321cba";

	check(strcmp(strrev(s), ex)==0, "strrev is failed.");

	return 0;

error:
	return 1;
}
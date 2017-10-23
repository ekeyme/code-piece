#include "str.h"
#include "dbg.h"
#include <string.h>

int main()
{
	char *s = "abc123";
	char *ex = "321cba";
	char out[100] = {'\0'}; 
	
	check(strcmp(strrev2(out, s, strlen(s)), ex)==0, "strrev2 is failed.");

	return 0;

error:
	return 1;
}
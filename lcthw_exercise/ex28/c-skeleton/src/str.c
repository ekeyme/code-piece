#include "str.h"
#include <stdlib.h>

char *strrev(char s[])
{
	char * const rs = s;
	char * left_s = s;
	char ch = '\0';

	// find the end of the string
	while(*s++);
	s -= 2;

	while(left_s < s) {
		ch = *left_s;

		*left_s++ = *s;
		*s-- = ch;
	}

	return rs;
}

char *strrev2(char *out, char *s, size_t len)
{	
	size_t i = 0;
	char *right = s + len - 1;
	*(out+len) = '\0';

	do
	{
		*(out+i) = *right;
		*(out+len-i-1) = *s;

		i++;
	} while (++s < --right);

	return out;
}

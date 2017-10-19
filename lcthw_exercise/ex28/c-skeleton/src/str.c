#include "str.h"

char *strrev(char *s)
{
	char * const rs = s;
	char * left_s = s;
	char ch = '\0';

	// find the end of the string
	while(*s++);
	s -= 2;

	while(rs < s) {
		ch = *left_s;

		*left_s++ = *s;
		*s-- = ch;
	}

	return rs;
}

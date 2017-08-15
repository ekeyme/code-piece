/** WARNING: This code is fress nd potentially isn't correct ye. */

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include "dbg.h"

#define MAX_DATA 10

int read_string(char *out_string, int max_buffer)
{
	log_info("out_string points to: %p", out_string);
	char *result = fgets(out_string, max_buffer, stdin);
	check(result != NULL, "Input error.");

	return 0;

error:
	return -1;
}

int read_int(long *out_int)
{
	char input[MAX_DATA];
	char *end = NULL;
	int rc = read_string(input, MAX_DATA);
	check(rc == 0, "Failed to read number");

	*out_int = strtol(input, &end, 10);
	check((*end == '\0' || *end == '\n') && input[0] != '\0', "Invalid number: %s", input);

	return 0;

error:
	return -1;
}

int read_scan(const char *fmt, ...)
{
	int i = 0;
	int rc = 0;
	long *out_int = NULL;
	char *out_char = NULL;
	char *out_string = NULL;
	int max_buffer = 0;

	va_list argp;
	va_start(argp, fmt);

	for(i = 0; fmt[i] != '\0'; i++) {
		if(fmt[i] == '%') {
			i++;
			switch(fmt[i]) {
				case '\0':
					sentinel("Invalid format, you ended with %%");
					break;

				case 'd':
					out_int = va_arg(argp, long *);
					rc = read_int(out_int);
					check(rc == 0, "Failed to read int.")
					break;

				case 'c':
					out_char = va_arg(argp, char *);
					*out_char = fgetc(stdin);
					break;

				case 's':
					max_buffer = va_arg(argp, int);
					log_info("max_buffer is: %d", max_buffer);
					out_string = va_arg(argp, char *);
					log_info("out_string points to: %p", out_string);
					rc = read_string(out_string, max_buffer);
					check(rc == 0, "Failed to read string.");
					break;

				default:
					sentinel("Invalid format.");
			}
		} else {
			fgetc(stdin);
		}

		check(!feof(stdin) && !ferror(stdin), "Input error");
	}

	va_end(argp);
	return 0;

error:
	va_end(argp);
	return -1;
}

int main(int argc, char *argv[])
{
	char first_name[MAX_DATA] = {'\0'};
	printf("first_name points to: %p\n", first_name);

	printf("What's you first name? ");
	int rc = read_scan("%s", MAX_DATA, first_name);
	check(rc == 0, "Failed first name.");

	printf("---- RESULTS ----\n");
	printf("First Name: '%s'", first_name);
	
	return 0;

error:
	return -1;
}

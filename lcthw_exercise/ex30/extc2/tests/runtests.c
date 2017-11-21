#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <glob.h>
#include "dbg.h"
#define MAX_CMD_LEN 1024

char *log_file = "build/tests.log";


int run_cmd(const char *arg0, ...)
{
	va_list argp;
	int cmd_len = 0;
	int arg_len = strlen(arg0);
	char cmd[MAX_CMD_LEN] = {'\0'};
	char *arg;

	check(cmd_len + arg_len < MAX_CMD_LEN, "cmd too long.");

	strncpy(&cmd[0], arg0, arg_len);
	cmd_len += arg_len;
	cmd[cmd_len++] = ' ';

	va_start(argp, arg0);
	while((arg = va_arg(argp, char *))) {
		arg_len = strlen(arg);

		check(cmd_len + arg_len < MAX_CMD_LEN, "cmd too long.");

		strncpy(&cmd[cmd_len], arg, arg_len);
		cmd_len += arg_len;
		cmd[cmd_len++] = ' ';
	}
	cmd[--cmd_len] = '\0';

	va_end(argp);

	return system(cmd);

error:
	return -1;
}

int main()
{
	char rm_cmd[255] = "rm -f";
	int rc;
	size_t i = 0;
	glob_t globbuf;

	printf("Running unit tests:\n");
	run_cmd(rm_cmd, log_file, (char *) NULL);

	rc = glob("tests/*_tests", 0, NULL, &globbuf);
	check(rc == 0, "Failed to glob tests files.");

	for(i = 0; i < globbuf.gl_pathc; ++i) {
		rc = run_cmd(globbuf.gl_pathv[i], "2>>", log_file, (char *) NULL);
		if(rc == 0) {
			printf("%s PASS\n", globbuf.gl_pathv[i]);
		} else {
			printf("runtests: ERROR in test %s: here's build/tests.log\n", 
				globbuf.gl_pathv[i]);
			printf("-----\n");
			run_cmd("tail", log_file, (char *) NULL);

			goto error;
		}
	}

	globfree(&globbuf);

	return 0;

error:
	globfree(&globbuf);
	return 1;
}

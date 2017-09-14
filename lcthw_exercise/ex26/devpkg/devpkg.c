#include <stdio.h>
#include <apr_general.h>
#include <apr_getopt.h>
#include <apr_strings.h>
#include <apr_lib.h>

#include "dbg.h"
#include "db.h"
#include "commands.h"

int main(int argc, char const *argv[])
{
	apr_pool_t *p = NULL;
	apr_pool_initialize();
	apr_pool_create(&p, NULL);

	apr_getopt_t *opt;
	apr_status_t rv;

	char ch = '\0';
	const char *optarg = NULL;
	const char *config_opts = NULL;
	const char *install_opts = NULL;
	const char *make_opts = NULL;
	const char *url = NULL;
	enum CommandType request = COMMAND_NONE;

	return 0;

error:
	return 1;
}
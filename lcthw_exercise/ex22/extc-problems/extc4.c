#include "dbg.h"

int recursive_func()
{
	int i = 0;
	log_info("i now is: %d", i++);
	if(i > 10) {
		return i;
	} else {
		// this uses out of the stack space
		return recursive_func();
	}
}

int main(int argc, char const *argv[])
{
	recursive_func();
	return 0;
}

#include "dbg.h"

void f_pass_by_value(int i)
{
	log_info("the argument value is: %d, its address is: %p", i, &i);
	// change value of i
	i = 99;
	log_info("the variable value now is: %d, its address is: %p", i, &i);
}

void f_pass_by_ref(int *i)
{
	log_info("the argument value is: %d, the address it pointed to is: %p", *i, i);
	// change value of i
	*i = 99;
	log_info("the variable value is: %d, the address it pointed to is: %p", *i, i);
}

int main(int argc, char *argv[])
{
	int i = 10;

	log_info("the value of i: %d, its address is: %p", i, &i);
	log_info("pass its value to f_pass_by_value");
	f_pass_by_value(i);
	log_info("after calling: the value of i: %d, its address is: %p", i, &i);

	printf("\n");
	log_info("pass its reference to f_pass_by_ref");
	f_pass_by_ref(&i);
	log_info("after calling: the value of i: %d, its address is: %p", i, &i);

	return 0;
}

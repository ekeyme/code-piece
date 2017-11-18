echo "Running unit tests:"

prog=tests/ex29_tests
lib=build/libex29.so
log=build/tests.log

rm -f $log

# test print_a_message
output=$($prog $lib print_a_message AbcD1 2>> $log)

if (($? == 0)) && [[ "$output" = "A STRING: AbcD1" ]]; then
	echo "$prog: print_a_message" PASS
else
	echo "ERROR in test $prog: print_a_message: here's $log"
	echo "-----"
	tail $log
	exit 1
fi 

# test uppercase
output=$($prog $lib uppercase AbcD1 2>> $log)

if (($? == 0)) && [[ "$output" = ABCD1 ]]; then
	echo "$prog: uppercase" PASS
else
	echo "ERROR in test $prog: uppercase: here's $log"
	echo "-----"
	tail $log
	exit 1
fi 

# test lowercase
output=$($prog $lib lowercase AbcD1 2>> $log)

if (($? == 0)) && [[ "$output" = abcd1 ]]; then
	echo "$prog: lowercase" PASS
else
	echo "ERROR in test $prog: lowercase: here's $log"
	echo "-----"
	tail $log
	exit 1
fi 

# test fail_on_purpose
output=$($prog $lib fail_on_purpose AbcD1 2>> $log)

if (($? == 1)) && [[ "$output" = "" ]]; then
	echo "$prog: fail_on_purpose" PASS
else
	echo "ERROR in test $prog: fail_on_purpose: here's $log"
	echo "-----"
	tail $log
	exit 1
fi 

# test non_exist_func
output=$($prog $lib non_exist_func AbcD1 2>> $log)

if (($? != 0)); then
	echo "$prog: non_exist_func" PASS
else
	echo "ERROR in test $prog: non_exist_func: here's $log"
	echo "-----"
	tail $log
	exit 1
fi 


echo ""

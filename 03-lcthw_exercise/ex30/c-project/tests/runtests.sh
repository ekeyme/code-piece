echo "Running unit tests:"

rm -f build/tests.log

for i in tests/*_tests; do
	if test -x $i; then
		if ./$i 2>> build/tests.log; then
			echo $i PASS
		else
			echo "runtests.sh: ERROR in test $i: here's build/tests.log"
			echo "-----"
			tail build/tests.log
			exit 1
		fi
	fi
done

echo ""

all: ex29 libex29.so

ex29: ex29.c
	cc -Wall -g -o ex29 ex29.c -ldl 

libex29.so: libex29.o
	cc -shared -o libex29.so libex29.o

clean:
	rm -rf libex29.o ex29 libex29.so *.dSYM
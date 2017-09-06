PREFIX?=/home/mozz/vm-share/opt
CFLAGS=-g -Wall -I${PREFIX}/include/apr-1
LDFLAGS=-L${PREFIX}/lib -lapr-1 -laprutil-1 -pthread 

all: devpkg

devpkg: bstrlib.o db.o shell.o commands.o

install: all
	install -d $(DESTDIR)/$(PREFIX)/bin/
	install devpkg $(DESTDIR)/$(PREFIX)/bin/

clean:
	rm -f *.o
	rm -f devpkg
	rm rf *.dSYM
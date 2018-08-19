PREFIX?=/usr/local
CFLAGS=-g -Wall -I/home/mozz/vm-share/opt/include/apr-1/ 
LDFLAGS=-L/home/mozz/vm-share/opt/lib -lapr-1 -pthread -laprutil-1

all: devpkg

devpkg: bstrlib.o db.o shell.o commands.o

install: all
	install -d $(DESTDIR)/$(PREFIX)/bin
	install devpkg $(DESTDIR)/$(PREFIX)/bin

clean:
	rm -f *.o
	rm -f devpkg
	rm -rf *.dSYM

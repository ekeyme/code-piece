CFLAGS = -g -Wall -I src $(OPTFLAGS)

SOURCES = src/libex29.c
OBJECTS = src/libex29.o

SO_TARGETS = build/libex29.so

TEST_SRC = $(wildcard tests/*_tests.c)
TESTS = $(patsubst %.c,%,$(TEST_SRC))


all: build $(SO_TARGETS) tests

build:
	@mkdir build

$(SO_TARGETS): $(OBJECTS)
	cc -shared -o $@ $^

.PHONY: tests
tests: $(TESTS)
	sh ./tests/runtests.sh

clean:
	rm -rf $(OBJECTS) $(SO_TARGETS) build/* $(TESTS)
	find . -name "*.gc*" -exec rm {} \;
	rm -rf `find . -name "*.dSYM" -print`
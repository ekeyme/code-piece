CFLAGS = -g -O2 -Wall -I src -DNDEBUG $(OPTFLAGS)

SOURCES=$(wildcard src/**/*.c src/*.c)
OBJECTS=$(patsubst %.c,%.o,$(SOURCES))

SO_TARGETS = build/libx.so

TEST_SRC = $(wildcard tests/*_tests.c)
TESTS = $(patsubst %.c,%,$(TEST_SRC))


all: build $(SO_TARGETS) tests

dev: CFLAGS = -g -Wall -Isrc -Wextra $(OPTFLAGS)
dev: all

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
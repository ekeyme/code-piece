#!/usr/bin/env bash

set -e

rm -rf ex24 ex24.dSYM
CFLAGS='-Wall -g -fsanitize=address' make ex24

./ex24 <<EOF
Ekeyme
Mo
27
5
999999999

EOF

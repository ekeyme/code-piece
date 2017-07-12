#!/usr/bin/env bash

set -e

db=/tmp/mozz.test.db

echo "create database"
./extc2 $db c 25 10
echo ""

echo "save mozz, gaojw, wujm into database"
./extc2 $db s 1 mozz zhongzhenmo@fulengen.com
./extc2 $db s 2 gaojw jinweigao@fulengen.com
./extc2 $db s 3 wujm jinmingwu@fulengen.com
echo ""

echo "print all"
./extc2 $db l
echo ""

echo "get mozz from database"
./extc2 $db g 1
echo ""

echo "delete mozz"
./extc2 $db d 1
echo ""

echo "print all again"
./extc2 $db l
echo ""

echo "set mozz_with_long_email with email(>25)"
./extc2 $db s 1 mozz_with_long_email zhongzhenmabcdefgkijklmnopqrstuvwxzy@fulengen.com 
echo 

echo "get mozz_with_long_email"
./extc2 $db g 1

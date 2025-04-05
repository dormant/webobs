#!/bin/bash
touch check_holdings.lock

export LC_ALL=C
./check_holdings.pl | sort -u > holdings.txt

rm check_holdings.lock

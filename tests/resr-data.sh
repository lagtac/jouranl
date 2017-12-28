#!/usr/bin/env sh
DIRS=201{6,5,4}-{12,11,10}-{29,23,2,12,1,5}
FILES={0209,1754,2332}-{today-i,this-is,what-would}.txt

mkdir -p `eval echo $DIRS` && touch `eval echo $DIRS/$FILES`


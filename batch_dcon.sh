#!/bin/sh

mkdir $2
for i in $1/*; do
    cp $i ./g
    ./stride $3 $4
    topath=$2/${i##*/}
    mv dcon.out ${topath%.geq}.out
done

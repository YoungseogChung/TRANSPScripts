#!/bin/sh

cd $1
cp $2 ./g
./stride $4 $5
mv dcon.out $3
echo Results of DCON stored at $3

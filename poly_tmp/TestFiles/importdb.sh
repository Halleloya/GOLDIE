#!/bin/bash

for file in ./*.json
do
    mongoimport --db poly --collection TD --file $file
    echo '$file imported!' 
done
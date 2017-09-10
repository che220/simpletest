#!/usr/bin/bash

scriptDir=$(dirname $0)
files=$(echo *)
forPacks=
for file in $files; do
    if [[ $file != *"-lib" ]]; then
	forPacks="$forPacks $file"
    fi
done
date=$(date +%Y%m%d)
zip -r cassandra_spark_${date}.zip $forPacks -x target

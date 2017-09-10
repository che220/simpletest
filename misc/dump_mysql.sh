#!/bin/bash

mac=192.168.0.2
options="-alrv --delete --modify-window=2 --progress --delete-excluded"

ts=$(date +%Y%m%d_%H%M%S)
dumpFile=$HOME/mysql-dumps/dump_${ts}.sql
#    echo "Enter hui's password for MySQL DB:"
mysqldump -u hui -phui amazon.com > $dumpFile
echo "Gzipping the DB dump ..."
gzip $dumpFile

scp -p ${dumpFile}.gz huiwang@${mac}:dumps

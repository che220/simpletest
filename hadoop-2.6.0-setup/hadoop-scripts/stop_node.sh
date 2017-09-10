#!/bin/bash

set -x
#set -av

unset HADOOP_HOME
. /home/hui/.bashrc

sbin=$HADOOP_HOME/sbin

shcmd=$sbin/yarn-daemon.sh
$shcmd --config $HADOOP_CONF_DIR stop nodemanager

shcmd=$sbin/hadoop-daemon.sh
$shcmd --config $HADOOP_CONF_DIR --script hdfs stop datanode

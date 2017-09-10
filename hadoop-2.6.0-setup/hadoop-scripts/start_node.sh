#!/bin/bash

set -x
#set -av

. /home/hui/.bashrc

sbin=$HADOOP_HOME/sbin

shcmd=$sbin/hadoop-daemon.sh
$shcmd --config $HADOOP_CONF_DIR --script hdfs start datanode

shcmd=$sbin/yarn-daemon.sh
$shcmd --config $HADOOP_CONF_DIR start nodemanager

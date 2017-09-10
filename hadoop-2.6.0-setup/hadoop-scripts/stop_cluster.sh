#!/bin/bash

set -x
set -av

sbin=$HADOOP_HOME/sbin
slaves=$(cat $HADOOP_CONF_DIR/slaves)

$sbin/yarn-daemon.sh stop proxyserver --config $HADOOP_CONF_DIR
$sbin/mr-jobhistory-daemon.sh stop historyserver --config $HADOOP_CONF_DIR

scriptDir=/home/hui/hadoop-scripts
cmd="$scriptDir/stop_node.sh"
for slave in $slaves; do
    ssh $slave "$cmd"
done

shcmd=$sbin/yarn-daemon.sh
$shcmd --config $HADOOP_CONF_DIR stop resourcemanager

shcmd=$sbin/hadoop-daemon.sh
$shcmd --config $HADOOP_CONF_DIR --script hdfs stop namenode

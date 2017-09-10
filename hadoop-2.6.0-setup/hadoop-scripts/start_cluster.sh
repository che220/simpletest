#!/bin/bash

set -x
set -av

sbin=$HADOOP_HOME/sbin
slaves=$(cat $HADOOP_CONF_DIR/slaves)

shcmd=$sbin/hadoop-daemon.sh
$shcmd --config $HADOOP_CONF_DIR --script hdfs start namenode

shcmd=$sbin/yarn-daemon.sh
$shcmd --config $HADOOP_CONF_DIR start resourcemanager

scriptDir=/home/hui/hadoop-scripts
cmd="$scriptDir/start_node.sh"
for slave in $slaves; do
    ssh $slave "$cmd"
done

$sbin/yarn-daemon.sh start proxyserver --config $HADOOP_CONF_DIR
$sbin/mr-jobhistory-daemon.sh start historyserver --config $HADOOP_CONF_DIR

#!/bin/bash

# assume Linux environment (including Mac OS)
export defaultRecipients="abc@abc"
export failureRecipient="abc@abc"

project_name=my_model
sys=$(uname -a)
PS1='[\w]\$ '
export timestamp=$(date +%Y%m%d%H%M%S)
dateStamp=$(date +%Y%m%d)

export PYTHON_BIN=$(which python3)
export DS_ROOT=$HOME/${project_name}
export DATA_CACHE_DIR=$HOME/${project_name}_cache
export MODEL_OUTPUT_DIR=$HOME/workspace/${project_name}
export logDir=$HOME/workspace/log
if [[ $sys == Darwin* ]]; then
    echo "running in Mac ..."
    export defaultRecipients=${USER}@abc
    export failureRecipient=${USER}@abc
fi
export PYTHONPATH=$PYTHONPATH:$DS_ROOT
mkdir -p $MODEL_OUTPUT_DIR
mkdir -p $logDir

echo "DS_ROOT: $DS_ROOT"
echo "logDir: $logDir"
echo "PYTHON_BIN: $PYTHON_BIN"
echo "PYTHONPATH: $PYTHONPATH"
echo "Data Cache: $DATA_CACHE_DIR"
echo "Default email recipients: $defaultRecipients"
echo "Failure email recipients: $failureRecipient"

# Two parameters:
#     toConsole: 0 - no, 1 - yes
#     filePrefix: if not to console, log file will be $logDir/${filePrefix}_${dateStamp}.log
function getLogFile
{
    local toConsole=$1
    local filePrefix=$2

    logFile=/dev/stdout
    if [ $toConsole -eq 0 ]; then
        logFile=$logDir/${filePrefix}_${dateStamp}.log
        touch $logFile
        chmod go+r $logFile
    fi
    echo "Log file: $logFile" > /dev/stderr
    echo $logFile
}

function runPythonScript
{
    local pyScript=$1
    local logFile=$2

    echo "===== $pyScript" >> $logFile
    $PYTHON_BIN $pyScript >> $logFile 2>&1

    if [ $? -ne 0 ]; then
        body="$pyScript failed"
        if [ $console -eq 0 ]; then
            subj="Failed (${project_name}): $pyScript"
            echo "$body" |mutt -s "$subj" -a $logFile -- $failureRecipient
            echo "failure email sent"
        else
            echo $body
        fi
        exit 1
    fi
}

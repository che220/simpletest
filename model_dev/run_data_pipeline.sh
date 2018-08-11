#!/bin/bash

function usage()
{
    echo "usage: $0 [-h] [-d] [-v] [TY] [month]"
    echo '    -h: show this help'
    echo '    -d: debug/mock-run mode'
    echo '    -v: output goes to console, instead of log file'
    exit 1
}

console=0
mockRun=0
while getopts ":hdv" opt; do
    case $opt in
        d) echo "option: debug/mock-run mode"; mockRun=1;;
        v) console=1; echo "option: no log file";;
        h) usage;;
    esac
done
shift $((OPTIND -1))
args=$@
echo "Arguments: $args"

scriptDir=$(dirname $0)
. $scriptDir/job_env.sh

logFile=$(getLogFile $console ${project_name}_data_pipeline)
finalMsg='<html><body>'
s3Dir=s3://my-s3/${project_name}/training/

#========================================
absDir=$(cd $scriptDir;pwd)
pyScript=$absDir/data/data_pipeline.py
runPythonScript "$pyScript" $logFile
finalMsg="${finalMsg}generated model data</body></html>"
echo $finalMsg
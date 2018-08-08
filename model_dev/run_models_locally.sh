#!/bin/bash

function usage()
{
    echo "usage: $0 [-h] [-v]"
    echo '    -h: show this help'
    echo '    -v: output goes to console, instead of log file'
    exit 1
}

console=0
while getopts ":hv" opt; do
    case $opt in
        v) console=1; echo "option: no log file";;
        h) usage;;
    esac
done
shift $((OPTIND -1))
args=$@
echo "Arguments: $args"

scriptDir=$(dirname $0)
. $scriptDir/job_env.sh

emails=$defaultRecipients
logFile=$(getLogFile $console ${project_name}_models)
finalMsg='<html><body>'

pyScript=train.py
echo "========== running $pyScript ==========" >> $logFile
cmd="$PYTHON_BIN $scriptDir/training/${pyScript}"
$cmd >> $logFile 2>&1
if [ $? -ne 0 ]; then
    body="Failed to build ${project_name} models"
    subj="${project_name}: Failed to build ${project_name} models"
    echo "$body" |mutt -s "$subj" -a $logFile -- $emails
    exit 1
fi
finalMsg="${finalMsg}built ${project_name} models</body></html>"

subj="${project_name}: Successfully ran models and deployed outputs"
echo "$finalMsg" |mutt -e "set content_type=text/html" -s "$subj" $emails

#!/bin/sh

#to show output in shell
#set -xv

#to make multiple logs with current date
#now=$(date +"%Y-%m-%d_%H:%M:%S")
#filename="/var/www/tripnscan/batch_logs/untranslated_items/${now}.json"
inputFilename="/var/www/tripnscan/batch_logs/untranslated_items.json"
inputFile=$(cat "$inputFilename")
outputFilename="/var/www/tripnscan/batch_logs/untranslated_items.json"
google_script_url="/home/ec2-user/untranslated_items_tool/google_login.py"
slack_script_url="/home/ec2-user/untranslated_items_tool/slack_post.sh"

result=$(curl -X POST \
  https://api.dev.tripnscan.com/select_api/find_changes \
  -H 'Authorization: Basic anFfYXBpOlBIYXVjdTd1c3B1' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d "@$inputFilename")

echo $result | python -mjson.tool > "${outputFilename}"

log_summary=$(printf "${outputFilename}" | python "${google_script_url}")

$slack_script_url "$log_summary"

#to have the log display with utf-8 decoded
#output=$(cat ${filename}) 
#printf "$output" > "${filename}"

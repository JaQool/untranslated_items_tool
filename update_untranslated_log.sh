#!/bin/sh

#to show output in shell
#set -xv

#to make multiple logs with current date
#now=$(date +"%Y-%m-%d_%H:%M:%S")
#filename="/var/www/tripnscan/batch_logs/untranslated_items/${now}.json"
inputFilename="/var/www/tripnscan/batch_logs/untranslated_items.json"

inputFile=$(cat "$inputFilename")

result=$(curl -X POST \
  https://api.dev.tripnscan.com/select_api/find_changes \
  -H 'Authorization: Basic anFfYXBpOlBIYXVjdTd1c3B1' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d "$inputFile")

outputFilename="/var/www/tripnscan/batch_logs/untranslated_items.json"

echo $result | python -mjson.tool > "${outputFilename}"

log_summary=$(printf "${outputFilename}" | python google_login.py)

./slack_post.sh "$log_summary"



#to have the log display with utf-8 decoded
#output=$(cat ${filename}) 
#printf "$output" > "${filename}"

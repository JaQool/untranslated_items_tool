#!/bin/bash

argument=${1}

# Usage: slackpost "<webhook_url>" "<channel>" "<message>"

webhook_url=https://hooks.slack.com/services/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
if [[ $webhook_url == "" ]]
then
        echo "No webhook_url specified"
        exit 1
fi

shift
channel=@kevin_mcdaniel
if [[ $channel == "" ]]
then
        echo "No channel specified"
        exit 1
fi

shift

text1='The list of untranslated items for the DEV environment has been updated. '
text2=' Check the details here: '
link='https://docs.google.com/spreadsheets/d/1mRU-3NgPgayN17x-sMnWRix3-C7NiiKjaMyDIgBtO40/edit?usp=sharing'

text=$text1$argument$text2$link

if [[ $text == "" ]]
then
        echo "No text specified"
        exit 1
fi

escapedText=$(echo $text | sed 's/"/\"/g' | sed "s/'/\'/g" )
json="{\"channel\": \"$channel\", \"text\": \"$escapedText\"}"

curl -s -d "payload=$json" "$webhook_url"


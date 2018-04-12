#! /bin/bash


source /Users/jiagangzhang/workspace/myownsync/py35/venv/bin/activate
cd /Users/jiagangzhang/PycharmProjects/gsheet-jira

export LC_ALL="en_US.UTF-8"
#locale > debug.log

/Users/jiagangzhang/workspace/myownsync/py35/venv/bin/python update_google_sheet.py --mm > update.log
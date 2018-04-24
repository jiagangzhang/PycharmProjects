#! /bin/bash


source /Users/jiagangzhang/workspace/myownsync/py35/venv/bin/activate
cd /Users/jiagangzhang/PycharmProjects/check_duplicate_style

export LC_ALL="en_US.UTF-8"
#locale > debug.log

/Users/jiagangzhang/workspace/myownsync/py35/venv/bin/python check_duplicate_sku.py > check_duplicate_`date "+%Y_%m_%d_%H_%M"`.log
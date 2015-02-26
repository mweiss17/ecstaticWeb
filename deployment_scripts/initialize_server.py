#!/bin/sh
filename=/home/ec2-user/sds/sds/settings/__init__.py 
fab migrate_database
sed -i 's/.preprod/.prod/g' $filename

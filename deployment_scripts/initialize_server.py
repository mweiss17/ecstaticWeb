#!/bin/sh
filename=/home/ec2-user/sds/sds/settings/__init__.py 
sed -i 's/.dev/.prod/g' $filename

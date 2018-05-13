#!/usr/bin/env bash

set -e 

cd $(dirname "$0")

time=$(cat time.val)
host=$(cat host.val)

sed -i "s/#time#/$time/" cronfile
sed -i "s/#host#/$host/" run-iperf.sh


/usr/bin/crontab cronfile

echo -n "cron job: "
/usr/bin/crontab -l

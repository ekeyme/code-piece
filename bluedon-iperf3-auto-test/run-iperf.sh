#!/usr/bin/env bash

set -e

outfile=result-summary.result
cd $(dirname "$0")

rm -f $outfile tcp.result udp.result

host=#host#

/usr/bin/iperf3 -c $host -t 600 -J > tcp.result
if (($? == 0)); then
	cat tcp.result | /usr/bin/python2 ./iperf3-jresult-parser.py tcp > $outfile
fi 

sleep 60

/usr/bin/iperf3 -c $host -t 600 -u -b 10G -l1398 -J > udp.result
if (($? == 0)); then
	cat udp.result | /usr/bin/python2 ./iperf3-jresult-parser.py udp >> $outfile
fi 

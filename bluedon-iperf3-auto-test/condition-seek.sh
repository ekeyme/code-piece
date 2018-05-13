#!/usr/bin/env bash

#set -e

bandwidth=(1 4 8 16)
pkg_sz=(64 1024 4096 16384 65536 131072 262144 524288 1048576)
window_sz=(64 128 256 416)
mss=(174 699 2796 5592 7000 9216)

for bw in ${bandwidth[@]}; do
	for sz in ${pkg_sz[@]}; do
		for ws in ${window_sz[@]}; do
			for ms in ${mss[@]}; do
				echo -ne "${bw}\t${sz}\t${ws}\t${ms}\t"
				j=$(iperf3 -c 10.10.10.15 -b${bw}G -l $sz -w ${ws}K -M ${ms} -J)
				echo "$j" | python2.7 iperf3-jresult-parser.py tcp
			done
		done
	done
done
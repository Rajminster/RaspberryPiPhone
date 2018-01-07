#!/bin/bash

   
if python3 phoneCase.py ; then   # Compile it atleast once.
    echo "Compiled"
fi


while true
do
    sum1="$(md5 phoneCase.py)"
    sleep 2
    sum2="$(md5 phoneCase.py)"
    if [ "$sum1" != "$sum2" ];
    then
        echo "Different. Recompiling."
        if python3 phoneCase.py ; then   # Compile it atleast once.
          echo "Compiled"
        fi
    fi
done

#!/bin/sh

# sequence of commands to validate ntpd clients and
# server behavior

TARGET=$1

# check sources
echo 'show list of peers'
echo
ntpq -p ${TARGET}
echo
echo 'show sysinfo':
echo
ntpdc -c sysinfo ${TARGET}
echo
echo 'show systats':
echo
ntpdc -c sysstats ${TARGET}
echo
echo 'show iostats':
echo
ntpdc -c iostats ${TARGET}
echo
echo 'show timerstats':
echo
ntpdc -c timerstats ${TARGET}
echo
echo 'traffic counts collected and maintained by the monitor facility':
echo
ntpdc -c monlist ${TARGET}

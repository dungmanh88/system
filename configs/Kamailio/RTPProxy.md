http://www.rtpproxy.org/


yum install epel-release
yum install rtpproxy

rtpproxy -F -l lb-ip -s udp:127.0.0.1:7722 -d DBUG:LOG_LOCAL0

# Check system
## Check disk space
```
ncdu
```
```
df -Th
```
```
du -h --max-depth=1 --exclude=/var
```

## Check disk IO
```
iotop
```
```
atop -d
```
```
df -Th
ioping -c 10 /dev/sda
```

## Check memory
```
free -m
```
```
atop -m
```

## Check slab
```
slabtop
```

## Check swap usage
```
atop -m
```
user view
```
smem -u
```
library view
```
smem -m
```
```
vmstat
```

## Check cpu
```
atop -s
```
```
atop -y
```

## Check process
system call view
```
strace <command>
```
time view
```
time <command>
```

## Check network
```
ss -t -a
```
```
ss -s
```
```
netstat -nato
```
listen socket
```
netstat -tulpn
```
filter by state
```
ss -4 state established|syn-sent|syn-recv|fin-wait-1|fin-wait-2|closed|closed-wait|last-ack|closing|all|connected|synchronized
```
connected : All the states except for listen and closed

synchronized : All the connected states except for syn-sent

## Check system overall
```
atop
```
```
top
```
```
htop
```
```
pt-summary
```
```
dmesg
```
```
/var/log/messages
```
```
/var/log/secure
```

## Check open file handler
```
pidof mysqld
17079
lsof -a -p 17079 | wc -l
112
```
overall file handler (any sort)
```
lsof | wc -l
```
overall file handler (in kernel)
```
sysctl fs.file-nr
```
maximum file handler for a specific process
```
cat /proc/`pidof mysqld`/limits | egrep '(processes|files)'
```
maximum file handler for a specific user
```
su - mysql
ulimit -Hn
ulimit -Sn
```
maximum file handler (overall)
```
sysctl fs.file-max
```

# Check mysqld
## Check mysql overall
```
pt-mysql-summary  --user root --password pass
```
```
mysqladmin -u root -p  status
```

# Debug shell
```
bash -x ./shellcode
```

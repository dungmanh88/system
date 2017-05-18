# Count open file handler
```
pidof mysqld
17079
lsof -a -p 17079 | wc -l
112
```

# Count overall file handler (any sort)
```
lsof | wc -l
```

# Count overall file handler (in kernel)
```
sysctl fs.file-nr
```
```
cat /proc/sys/fs/file-nr
```

# Get maximum file handler for a specific process
```
cat /proc/`pidof mysqld`/limits | egrep '(processes|files)'
```

# Get maximum file handler for a specific user
```
su - mysql
ulimit -Hn
ulimit -Sn
```

# Get maximum file handler (overall)
```
sysctl fs.file-max
```
```
cat /proc/sys/fs/file-max
```

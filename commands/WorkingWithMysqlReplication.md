# Skip slave counter
```
mysql> stop slave;
mysql> set global SQL_SLAVE_SKIP_COUNTER = 1;
mysql> start slave;
```

# Skip errors
```
Enter your config
slave_skip_errors = <error_id_1[,error_id_2]>
then restart
```

# Show slave hosts from master
```
mysql> show slave hosts;
```

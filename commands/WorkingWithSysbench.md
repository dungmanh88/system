```
sysbench --num-threads=4 --max-requests=0 --max-time=10 \
--test=oltp --db-driver=mysql \
--mysql-user=sample --mysql-password=Sample1! \
--mysql-host=192.168.10.125 --mysql-port=6033 \
--mysql-db=sample \
--oltp-read-only=off prepare;
```

create table sbtest in sample db

```
sysbench --num-threads=4 --max-requests=0 --max-time=10 \
--test=oltp --db-driver=mysql \
--mysql-user=sample --mysql-password=Sample1! \
--mysql-host=192.168.10.125 --mysql-port=6033 \
--mysql-db=sample \
--oltp-read-only=off run;
```

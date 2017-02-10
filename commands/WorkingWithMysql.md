## Proccess - Thread - Connections

### Get total current connections
Because mysql's one-thread-per-connection:
```
mysql> show global status like '%thread_connect%';
mysql> show global status like '%thread_running%';
```

### Show processlist
```
mysql> show full processlist;
```

## Dump - Backup - Restore

### Lock tables before dumping
```
mysql -u root -p -Ane "flush tables with read lock; select sleep(86400);"
```

### Dump metadata
```
mysqldump -u root -p --single-transaction --routines --triggers --events --no-data --master-data=2 --databases <db1[, db2, db3]> --extended-insert --quick --log-error=/tmp/<dbname>.nodata.dump.log > /root/<dbname>.nodata.dump
```

## DDL - metadata

### Offline alter table
alter statement - use if table is small

### Online alter table
pt-online-schema-change - use if table if large

### Show structure table
```
mysql> show create table <table_name>
```

## User management

### Default grant web account
```
mysql> grant index, create temporary tables, create view, show view, create routine, alter routine, trigger, delete, insert, select, update, execute on `db`.* to 'user'@'host' identified by 'auth_string';
mysql> flush privileges;
```

### Default grant phpmyadmin account
```
mysql> grant create, alter, drop, index, create temporary tables, create view, show view, create routine, alter routine, trigger, delete, insert, select, update, execute on `db`.* to 'user'@'host' identified by 'auth_string';
mysql> flush privileges;
```

### Grant account with unknown passwd
```
mysql> grant index, create temporary tables, create view, show view, create routine, alter routine, trigger, delete, insert, select, update, execute on `db`.* to 'user'@'host' identified by password 'hash_string';
mysql> flush privileges;
```

### Revoke grants
```
mysql> revoke all on `db`.* from 'user'@'host';
```

### Show all grants
```
pt-show-grants --user=root --ask-pass > mysql.users.clone.sql
```

### Show grant for a specific user
```
mysql> show grants for 'user'@'host';
```

### Set password
```
mysql> alter user 'user'@'host' identified by 'auth_string';
or
mysql> set password for 'user'@'host' = password('auth_string');
or for current user
mysql> alter user user() identified by 'auth_string';
```

### Reset root password
```
service mysqld start --skip-grant-tables --skip-networking
mysql
mysql> flush privileges;
mysql> alter user 'root'@'localhost' identified by 'auth_string';
or
mysql> set password for 'root'@'localhost' = password('auth_string');
```

## Filter
```
mysql> pager less
reference to `which less` command on OS
mysql> show engine innodb status\G
```

## Work with datadir

### Re-initialize mysql datadir
```
mysql 5.6 and earlier
mysql_install_db
chown -R mysql:mysql /var/lib/mysql
```

```
mysql 5.7 and later
mysqld --initialize
chown -R mysql:mysql /var/lib/mysql
```

## Debug

### Get overview information
```
mysqladmin status
pt-mysql-summary
view percona monitoring and management
```

## Collation
```
show collation like 'utf8%';
select _utf8'ê' collate utf8_unicode_520_ci = _utf8'e' collate utf8_unicode_520_ci as equal;
```

## Replication

### Skip slave counter
```
mysql> stop slave;
mysql> set global SQL_SLAVE_SKIP_COUNTER = 1;
mysql> start slave;
```

### Skip errors
```
Enter your config
slave_skip_errors = <error_id_1[,error_id_2]>
then restart
```

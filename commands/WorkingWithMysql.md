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

## DDL - metadata

### Offline alter table
alter statement - use if table is small

### Online alter table
pt-online-schema-change - use if table if large

### Show structure table
```
mysql> show create table <table_name>
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

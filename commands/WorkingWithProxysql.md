# Login
```
mysql -u admin -padmin -h 127.0.0.1 -P6032
\R Admin>
```

# Verify config
```
Admin>SELECT * FROM mysql_servers;
Empty set (0.00 sec)

Admin>SELECT * from mysql_replication_hostgroups;
Empty set (0.00 sec)

Admin>SELECT * from mysql_query_rules;
Empty set (0.00 sec)

Admin>SELECT * from mysql_users;
Empty set (0.00 sec)
```

# Config servers
```
insert into mysql_servers(hostgroup_id, hostname, port, max_connections, max_replication_lag) values (0, '192.168.10.123', 3306, 512, 300);
insert into mysql_servers(hostgroup_id, hostname, port, max_connections, max_replication_lag) values (1, '192.168.10.122', 3306, 512, 300);
insert into mysql_servers(hostgroup_id, hostname, port, max_connections, max_replication_lag) values (1, '192.168.10.124', 3306, 512, 300);

insert into mysql_servers(hostgroup_id, hostname, port, max_connections, max_replication_lag) values (2, '192.168.10.223', 3306, 512, 300);
insert into mysql_servers(hostgroup_id, hostname, port, max_connections, max_replication_lag) values (2, '192.168.10.224', 3306, 512, 300);
```

# Config users
```
insert into mysql_users(username, password, active, default_hostgroup, default_schema, max_connections) values('sample','sample',1, 0, 'sample', 512)
insert into mysql_users(username, password, active, default_hostgroup, default_schema, max_connections) values('example','example',1, 2, 'example', 512);
```

# Query statistic
```
SELECT * FROM stats_mysql_commands_counters WHERE Total_cnt >0;

SELECT rule_id, match_pattern, hits FROM mysql_query_rules LEFT JOIN stats_mysql_query_rules USING (rule_id);

SELECT * FROM stats_mysql_query_digest ORDER BY sum_time DESC;

select hostgroup, digest_text, count_star, sum_time, min_time, max_time from stats_mysql_query_digest order by sum_time desc LIMIT 10;
```

# Show stats table structure
```
SHOW TABLES FROM stats;
show create table stats.stats_mysql_processlist;
```

# Check process list
```
select * from stats_mysql_processlist
```

# Check connection pool
```
select * from stats_mysql_connection_pool
```

# Check runtime
```
select * from runtime_mysql_servers;
select * from runtime_mysql_query_rules;
select * from runtime_mysql_replication_hostgroups;
select * from runtime_mysql_users;
select * from runtime_scheduler;
select * from runtime_global_variables;
```

# Check sqlitedb
```
sqlite3 /var/lib/proxysql/proxysql.db
```

# Where is proxysql db
```
/var/lib/proxysql/proxysql.db
```

# Check log
```
tail -f /var/lib/proxysql/proxysql.log
```

# Test backend
```
mysql -uexample -pExample1! -h 192.168.10.125 -P 6033 -e "SELECT @@hostname"
```

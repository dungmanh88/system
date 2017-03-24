# Default grant web account
```
mysql> grant index, create temporary tables, create view, show view, create routine, alter routine, trigger, delete, insert, select, update, execute on `db`.* to 'user'@'host' identified by 'auth_string';
mysql> flush privileges;
```

# Default grant phpmyadmin account
```
mysql> grant create, alter, drop, index, create temporary tables, create view, show view, create routine, alter routine, trigger, delete, insert, select, update, execute on `db`.* to 'user'@'host' identified by 'auth_string';
mysql> flush privileges;
```

# Grant account with unknown passwd
```
mysql> grant index, create temporary tables, create view, show view, create routine, alter routine, trigger, delete, insert, select, update, execute on `db`.* to 'user'@'host' identified by password 'hash_string';
mysql> flush privileges;
```

# Revoke grants
```
mysql> revoke all on `db`.* from 'user'@'host';
```

# Show all grants
```
pt-show-grants --user=root --ask-pass > mysql.users.clone.sql
```

# Show grant for a specific user
```
mysql> show grants for 'user'@'host';
```

# Set password
```
mysql> alter user 'user'@'host' identified by 'auth_string';
or
mysql> set password for 'user'@'host' = password('auth_string');
or for current user
mysql> alter user user() identified by 'auth_string';
```

# Reset root password
```
service mysqld start --skip-grant-tables --skip-networking
mysql
mysql> flush privileges;
mysql> alter user 'root'@'localhost' identified by 'auth_string';
or
mysql> set password for 'root'@'localhost' = password('auth_string');
```

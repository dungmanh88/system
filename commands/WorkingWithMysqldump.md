# Lock tables before dumping
```
mysql -u root -p -Ane "flush tables with read lock; select sleep(86400);"
```

# Dump metadata
```
mysqldump -u root -p --single-transaction --routines --triggers --events --no-data --master-data=2 --databases <db1[, db2, db3]> --extended-insert --quick --log-error=/tmp/<dbname>.nodata.dump.log > /root/<dbname>.nodata.dump
```

# Dump databases
```
mysqldump -u root -p --single-transaction --routines --triggers --events --add-drop-database --add-drop-table --databases <dbname> --master-data=2 --extended-insert --quick --log-error=/tmp/<dbname>.dump.log > /root/<dbname>.dump
```

# Import ignore error
```
mysql -u root -p -f < file.dump
```

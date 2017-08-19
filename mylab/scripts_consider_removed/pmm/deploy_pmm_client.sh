#!/bin/bash

set -x

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

pmm_url=http://www.percona.com/downloads/percona-release/redhat/0.1-4/percona-release-0.1-4.noarch.rpm
pmm_server=
pmm_user=
pmm_passwd=
mysql_user=
mysql_passwd=
mysql_port=3306
mysql_host=127.0.0.1

mongo_user=
mongo_passwd=
mongo_port=27017
mongo_host=127.0.0.1
mongo_db=admin
mongo_uri=mongodb://${mongo_user}:${mongo_passwd}@${mongo_host}:${mongo_port}/${mongo_db}

yum -y install ${pmm_url} && yum -y install pmm-client
pmm-admin config --server ${pmm_server} --server-user ${pmm_user} --server-password ${pmm_passwd} --server-insecure-ssl

ps -lef | grep mysqld | grep -v "grep"
[ $? -eq 0 ] && pmm-admin add mysql --host=${mysql_host} --user ${mysql_user} --port ${mysql_port} --password ${mysql_passwd}

ps -lef | grep mongod | grep -v "grep"
if [[ $? -eq 0 && ! -z mongo_user && ! -z mongo_passwd ]]; then
  pmm-admin add mongodb --uri ${mongo_uri}
fi

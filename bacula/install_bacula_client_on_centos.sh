#!/bin/bash

set -e

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

BACULA_VERSION=7.4.0
BACULA_DOWNLOAD="http://downloads.sourceforge.net/project/bacula/bacula/${BACULA_VERSION}/bacula-${BACULA_VERSION}.tar.gz"
TEMP_INSTALLATION=/tmp
DEFAULT_INSTALLTION=/usr/local/bin/bacula/bin
BACULA_SERVICE_DIR_NAME=my-backup-dir
BACULA_SERVICE_DIR_PASSWD=pass1
BACULA_SERVICE_MON_NAME=my-backup-mon
BACULA_SERVICE_MON_PASSWD=pass2
BACULA_FILE_DAEMON_NAME=my-backup-fd
BACULA_DIR_ADDRESS=192.168.10.255
BACULA_DIR_NAME=backup.me

function install_dependencies() {
  echo "INSTALL DEPENDENCIES"
  yum -y install zlib zlib-devel openssl openssl-devel gcc gcc-c++
  echo "INSTALL DEPENDENCIES DONE!!!"
}

function download_and_extract_package() {
  echo "DOWNLOAD AND EXTRACT"
  rm -rf ${TEMP_INSTALLATION}/bacula-${BACULA_VERSION}.tar.gz
  rm -rf ${TEMP_INSTALLATION}//bacula-${BACULA_VERSION}
  cd ${TEMP_INSTALLATION}
  curl -OL ${BACULA_DOWNLOAD}
  tar xvzf bacula-${BACULA_VERSION}.tar.gz
  echo "DOWNLOAD AND EXTRACT DONE!!!"
}

function install_package() {
  echo "INSTALLING"
  cd ${TEMP_INSTALLATION}/bacula-${BACULA_VERSION}
  CFLAGS="-g -O2"
 ./configure \
            --sbindir=/usr/local/bin/bacula/bin \
            --sysconfdir=/usr/local/bin/bacula/bin \
            --with-pid-dir=/usr/local/bin/bacula/bin/working \
            --with-subsys-dir=/usr/local/bin/bacula/bin/working \
            --enable-smartalloc \
            --enable-client-only \
            --with-working-dir=/usr/local/bin/bacula/bin/working && make && make install
  echo "INSTALL DONE!!!"
}

function install_ini_script() {
  echo "INSTALL INIT SCRIPT"
  cp ${DEFAULT_INSTALLTION}/bacula-ctl-fd /etc/init.d/
  sed -i '2i# chkconfig: - 30 60 2' /etc/init.d/bacula-ctl-fd
  chkconfig bacula-ctl-fd on
  service bacula-ctl-fd start
  echo "INSTALL INIT SCRIPT DONE!!!"
}

function config_client() {
  echo "CONFIG CLIENT"
  find /usr/local/bin/bacula/bin/* -maxdepth 0 | grep -v -i -E '(bacula-fd|bacula-ctl-fd|working)' | xargs rm
  local bacula_client_cnf=${DEFAULT_INSTALLTION}/bacula-fd.conf
  cat << EOF > ${bacula_client_cnf}
#
# List Directors who are permitted to contact this File daemon
#
Director {
  Name = ${BACULA_SERVICE_DIR_NAME}
  Password = "${BACULA_SERVICE_DIR_PASSWD}"
}

#
# Restricted Director, used by tray-monitor to get the
#   status of the file daemon
#
Director {
  Name = ${BACULA_SERVICE_MON_NAME}
  Password = "${BACULA_SERVICE_MON_PASSWD}"
  Monitor = yes
}

#
# "Global" File daemon configuration specifications
#
FileDaemon {                          # this is me
  Name = ${BACULA_FILE_DAEMON_NAME}
  FDport = 9102                  # where we listen for the director
  WorkingDirectory = /usr/local/bin/bacula/bin/working
  Pid Directory = /usr/local/bin/bacula/bin/working
  Maximum Concurrent Jobs = 20
# Plugin Directory = /usr/lib64
}

# Send all messages except skipped files back to Director
Messages {
  Name = Standard
  director = ${BACULA_SERVICE_DIR_NAME} = all, !skipped, !restored
}
EOF
  echo "${BACULA_DIR_ADDRESS} ${BACULA_DIR_NAME}" >> /etc/hosts
  service bacula-ctl-fd restart
  echo "CONFIG CLIENT DONE!!!"
}

function main() {
  install_dependencies \
  && download_and_extract_package \
  && install_package \
  && install_ini_script \
  && config_client
}

main

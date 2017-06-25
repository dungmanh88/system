#!/bin/bash

generate_salt() {
  cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 48 | head -n 1
}

DB_HOST=${DB_HOST:-mysql_mattermost_swat}
DB_PORT_NUMBER=${DB_PORT_NUMBER:-3306}
MM_USERNAME=${MM_USERNAME:-mmuser}
MM_PASSWORD=${MM_PASSWORD:-mmuser_password}
MM_DBNAME=${MM_DBNAME:-mattermost}
MM_DIR=/opt/mattermost
MM_CONFIG=${MM_DIR}/config/config.json
MM_SITE_URL=${MM_SITE_URL:-mm.swat.example.com}

if [ -f $MM_CONFIG ]
   then
     # Substitue some parameters with jq
     jq '.ServiceSettings.SiteURL = "'http://${MM_SITE_URL}'"' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.LogSettings.EnableConsole = false' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.LogSettings.ConsoleLevel = "INFO"' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.FileSettings.Directory = "'${MM_DIR}/data/'"' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.FileSettings.EnablePublicLink = true' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.FileSettings.PublicLinkSalt = "'$(generate_salt)'"' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.SqlSettings.DriverName = "mysql"' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.SqlSettings.DataSource = "'${MM_USERNAME}:${MM_PASSWORD}@tcp'('${DB_HOST}:${DB_PORT_NUMBER}')'/${MM_DBNAME}'?charset=utf8mb4,utf8&readTimeout=30s&writeTimeout=30s''"' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
     jq '.SqlSettings.AtRestEncryptKey = "'$(generate_salt)'"' $MM_CONFIG > $MM_CONFIG.tmp && mv $MM_CONFIG.tmp $MM_CONFIG
   fi


# For the first time, I must wait db
echo "Wait until database $DB_HOST:$DB_PORT_NUMBER is ready..."
until nc $DB_HOST $DB_PORT_NUMBER
do
    echo -ne "."
    sleep 1
done

sleep 1
echo "Starting platform"
exec "$@"

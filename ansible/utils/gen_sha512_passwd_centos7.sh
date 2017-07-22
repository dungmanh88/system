#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "You must run as root"
  exit 1
fi

which pip
if [ ! $? -eq 0 ]; then
  echo "You must install pip"
  exit 1
fi

pip install passlib

set -e
/usr/bin/python -c "from passlib.hash import sha512_crypt; import getpass; print sha512_crypt.encrypt(getpass.getpass())"

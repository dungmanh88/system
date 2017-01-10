#!/bin/bash
set -e
/usr/local/bin/python2.7 -c "from passlib.hash import sha512_crypt; import getpass; print sha512_crypt.encrypt(getpass.getpass())"

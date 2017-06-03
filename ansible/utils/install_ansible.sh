#!/bin/bash

set -e

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

echo "=================== Setup ansible ==================="

yum -y install epel-release \
&& yum -y install ansible git-all gcc gcc-c++ python-devel mariadb-devel openssl-devel wget python-cffi libffi-devel

cat /etc/*release | grep -q "7\."
if [ $? -eq 0 ]; then
  if [ ! -f /tmp/get-pip.py ]; then
      wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py
  fi
  ### support ansible vault
  # then
  ### generate crypted passwords for the user module
  python /tmp/get-pip.py \
  && pip install cryptography \
  && pip install passlib
fi

mkdir -p /etc/.ssh && \
echo -e  'y\n' | ssh-keygen -t rsa -N "" -f /etc/.ssh/ansible_id_rsa

touch /etc/.vault_pass.txt
echo "Your vault passwd: "
read vault_pass
echo "You entered: ${vault_pass}"
echo ${vault_pass} > /etc/.vault_pass.txt

echo "=================== Create gen_sha512_password file ==================="

genpass_file=/etc/ansible/gen_sha512_password.sh

cat << EOF > ${genpass_file}
#!/bin/bash
set -e
/usr/bin/python -c "from passlib.hash import sha512_crypt; import getpass; print sha512_crypt.encrypt(getpass.getpass())"
EOF

chmod u+x ${genpass_file}

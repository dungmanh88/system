#!/bin/bash

echo "=================== Setup deployer user ==================="

deployer_user=deployer
deployer_group=ansible
gw=""

ssh_dir=/home/${deployer_user}/.ssh
authorized_keys=${ssh_dir}/authorized_keys
sshd_cnf=/etc/ssh/sshd_config

# Set gw
if route -n | grep -q UG; then
  echo "default gw is set"
else
  route add default gw ${gw}
fi

# Create user
if grep -q ${deployer_user} /etc/passwd; then
  echo "user ${deployer_user} is exists"
else
  useradd ${deployer_user}
fi

# Create group
if grep -q ${deployer_group} /etc/group; then
  echo "user ${deployer_group} is exists"
else
  groupadd ${deployer_group}
fi

# Create sudoers
cat << EOF > /etc/sudoers.d/${deployer_group}
%${deployer_group} ALL=(ALL:ALL) ALL
EOF

# Add user into group
usermod -aG ${deployer_group} ${deployer_user}

# Key based authentication
mkdir -p ${ssh_dir} && chmod 700 ${ssh_dir} \
&& touch ${authorized_keys}

cat << EOF > ${authorized_keys}
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4TsLZgY3pMe7yRUPfDV32It5VD+/Sb0HM2SqexWswUOjtKQMVYVhsmTEYvSsBl1CPc+15WeNLfCMxd6pvZhWKDQnb1FOJtYiIPxNBFWunk2M3rM23s/4CzKnUdJoJqZM4l2XliB5G+95lcT3sw6Ar/KeZNeGpMiqmf0V2YavBe22TAG0Lx1XagRLB+2byV2OAGFdVWjdWYZ/GEzt2bc7+imRSTXnn6TNqX0JqTey5FjSbhiFHJkkxqhxHbbKSjIEL/+OjBBgyDQKkhsZmnyY+vrkamr+1tIaGVRE9TA+Md9keqoVSN6z4IOYm7EDV0qUSbrfPCNpGq7tnyGeNfcYN ansible@devops
EOF

chmod 600 ${authorized_keys} && chown -R ${deployer_user}:${deployer_user} ${ssh_dir}

# Set passwd
passwd ${deployer_user}

# Secure sshd
sed -i '/^#Port/s/#Port/Port/' ${sshd_cnf} && \
sed -i '/^Port/s/22/1102/' ${sshd_cnf} && \
sed -i '/^#Protocol/s/#Protocol/Protocol/' ${sshd_cnf} && \
sed -i '/^#PermitRootLogin/s/#PermitRootLogin/PermitRootLogin/' ${sshd_cnf} && \
sed -i '/^PermitRootLogin/s/yes/no/' ${sshd_cnf} && \
sed -i '/^#PermitEmptyPasswords/s/#PermitEmptyPasswords/PermitEmptyPasswords/' ${sshd_cnf} && \
sed -i '/^PermitEmptyPasswords/s/yes/no/' ${sshd_cnf} && \
sed -i '/^#PasswordAuthentication/s/PasswordAuthentication/PasswordAuthentication/' ${sshd_cnf} && \
sed -i '/^PasswordAuthentication/s/yes/no/' ${sshd_cnf}

if grep -q "AllowGroups ${deployer_group}" ${sshd_cnf}; then
  echo "Allowed groups ${deployer_group} in ${sshd_cnf}"
else
  echo "AllowGroups ${deployer_group}" >> ${sshd_cnf}
fi

systemctl enable sshd && systemctl restart sshd

# Disable selinux
if sestatus | grep -q "disabled"; then
  echo "disabled selinux"
else
  setenforce 0
fi

# Disable firewalld
systemctl disable firewalld && systemctl stop firewalld

# Lock down cronjob
grep -q -F "ALL" /etc/cron.deny || echo "ALL" >>/etc/cron.deny

# Disable ipv6 and broadcast msg, echo ping msg on centos 7
grep -q -F "net.ipv6.conf.all.disable_ipv6 = 1" /etc/sysctl.conf || echo "net.ipv6.conf.all.disable_ipv6 = 1" >> /etc/sysctl.conf
grep -q -F "net.ipv6.conf.default.disable_ipv6 = 1" /etc/sysctl.conf || echo "net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf
grep -q -F "net.ipv4.icmp_echo_ignore_all = 1" /etc/sysctl.conf || echo "net.ipv4.icmp_echo_ignore_all = 1" >> /etc/sysctl.conf
grep -q -F "net.ipv4.icmp_echo_ignore_broadcasts = 1" /etc/sysctl.conf || echo "net.ipv4.icmp_echo_ignore_broadcasts = 1" >> /etc/sysctl.conf
sysctl -p

# Remove user with empty password
if [ ! -z "$(cat /etc/shadow | awk -F: '($2==""){print $1}')" ]; then
  cat /etc/shadow | awk -F: '($2==""){print $1}' >> /var/log/secure_user_linux
  cat /etc/shadow | awk -F: '($2==""){print $1}' | xargs userdel -r &> /dev/null
fi

# Lock root
passwd -l root \
&& usermod -s /sbin/nologin root

# Remove x window package
yum -y groupremove "X Window System"

# Update
yum update -y

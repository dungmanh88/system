#!/bin/bash

echo "=================== Setup deployer user ==================="

deployer_user=deployer
deployer_group=ansible
ssh_dir=/home/${deployer_user}/.ssh
authorized_keys=${ssh_dir}/authorized_keys
sshd_cnf=/etc/ssh/sshd_config
jail_cnf_orig=/etc/fail2ban/jail.conf
jail_cnf=/etc/fail2ban/jail.local
iptables_jail_cnf=/etc/fail2ban/jail.d/00-ssh-iptables.conf

if grep -q ${deployer_user} /etc/passwd; then
  echo "user ${deployer_user} is exists"
else
  useradd ${deployer_user}
fi

if grep -q ${deployer_group} /etc/group; then
  echo "user ${deployer_group} is exists"
else
  groupadd ${deployer_group}
fi

cat << EOF > /etc/sudoers.d/${deployer_group}
%${deployer_group} ALL=(ALL:ALL) ALL
EOF

usermod -aG ${deployer_group} ${deployer_user}

passwd -l root \
&& usermod -s /sbin/nologin root

mkdir -p ${ssh_dir} && chmod 700 ${ssh_dir} \
&& touch ${authorized_keys}

cat << EOF > ${authorized_keys}
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDJwk58yR0iuSLERzk3EOPvRe9TQ40lt05fzYzOqPwThc9ibAFsysNe+lqQBtXmXXic35FZBQ8MOSEF+/XhMeiSs7tGOUsnRbJYdlr2mqiXAoqgJQzHkRa6rLvNpKulZF5URqW/mB8Ojw6PLZgBJ3YxCcacAgiBkhsNgSBwJoP4bcuhRQQ3tUYyqXbg39dtm6r7xP1rLAnuOizcQvGfuHY/Z27sDBk/l9p8t0HMYRkpDZZeZ37vFShuJp2tJ+rGJvNEfYjnYp/ezEye8AzF6Qh9dX2rH1i05pm9/8cLj1EOdkVoiI6XS4+z5yJ/M56HB0nyfzft/PSFTiO0fLW9xYs7 ansible@devops
EOF

chmod 600 ${authorized_keys} && chown -R ${deployer_user}:${deployer_user} ${ssh_dir}

sed -i '/^#Port/s/#Port/Port/' ${sshd_cnf} && \
sed -i '/^Port/s/22/1102/' ${sshd_cnf} && \
sed -i '/^#Protocol/s/#Protocol/Protocol/' ${sshd_cnf} && \
sed -i '/^#PermitRootLogin/s/#PermitRootLogin/PermitRootLogin/' ${sshd_cnf} && \
sed -i '/^PermitRootLogin/s/yes/no/' ${sshd_cnf} && \
sed -i '/^#PermitEmptyPasswords/s/#PermitEmptyPasswords/PermitEmptyPasswords/' ${sshd_cnf} && \
sed -i '/^PermitEmptyPasswords/s/yes/no/' ${sshd_cnf} && \
sed -i '/^#PasswordAuthentication/s/PasswordAuthentication/PasswordAuthentication/' ${sshd_cnf} && \
sed -i '/^PasswordAuthentication/s/yes/no/' ${sshd_cnf}

if grep -q "AllowUsers ${deployer_user}" ${sshd_cnf}; then
  echo "Allowed user ${deployer_user} in ${sshd_cnf}"
else
  echo "AllowUsers ${deployer_user}" >> ${sshd_cnf}
fi

if sestatus | grep -q "disabled"; then
  echo "disabled selinux"
else
  setenforce 0
fi

systemctl enable sshd && systemctl restart sshd


# Remove x window package
yum -y groupremove "X Window System"

# Update
yum update -y

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

passwd ${deployer_user}

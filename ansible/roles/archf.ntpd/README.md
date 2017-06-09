# ansible-ntpd

Install and configure ntpd on a target host.

## Requirements

### Ansible version

Minimum required ansible version is 1.9.

## Description

Install and configure ntpd on rhel and debian hosts. This is only suitable
for client-server mode. Target can either be a ntpd server or a ntpd client.

Settings above work well for simple ntp clients.  See `templates/ntp.conf.j2`
for other defaults.


## Role Variables

### Variables conditionally loaded

Those variables from `vars/*.{yml,json}` are loaded dynamically during task
runtime using the `include_vars` module.

Variables loaded from `vars/Suse.yml`.

```yaml
ntpd_pkgs:
  - python-selinux
  - ntp

ntpd_svc_name: ntp

# Deliberately left indefined.
# see https://bugzilla.novell.com/show_bug.cgi?id=542098
# ntpd_keysfile: "/etc/ntp.keys"

```

Variables loaded from `vars/Debian.yml`.

```yaml
ntpd_pkgs:
  - ntp

ntpd_svc_name: ntp

ntpd_keysfile: "/etc/ntp/keys"

```

Variables loaded from `vars/RedHat.yml`.

```yaml
ntpd_pkgs:
  - ntp

ntpd_svc_name: ntpd

ntpd_keysfile: "/etc/ntp/keys"

```

### Default vars

Defaults from `defaults/main.yml`.

```yaml
# Enable/disable ntpd service.
ntpd_enabled: yes

# Stop/start ntpd service
ntpd_state: "started"

# Define ntpd sources. The [0-3].pool.ntp.org names point to a random set of
# servers that will change every hour.
ntpd_sources:
  - 0.pool.ntp.org
  - 1.pool.ntp.org
  - 2.pool.ntp.org
  - 3.pool.ntp.org

# Install (`present', `latest'), or remove (`absent') a package.
ntpd_pkg_state: latest

# Restrict statements within `ntpd_restrict` will relax defaults from
# configuration file template which are:
#   *restrict -4 default limited kod nomodify notrap nopeer noquery
#   *restrict -6 default limited kod nomodify notrap nopeer noquery

# By default, client hosts on local network are less restricted. Override this
# for more specifics needs. Elements of this list will be literally inserted
# into ntp.conf. You could define defaults for those for each of your dev,
# staging and production environnement and also create groups for your stratum
# servers.
ntpd_restrict:
  - restrict 10.0.0.0 mask 255.0.0.0 nomodify notrap nopeer
  - restrict 192.168.0.0 mask 255.255.0.0 nomodify notrap nopeer
  - restrict 172.16.0.0 mask 255.240.0.0 nomodify notrap nopeer

# no stats logging
ntpd_log_stats: no

# undefined crypto settings
# ntpd_crypto: ''

```


## Installation

### Install with Ansible Galaxy

```shell
ansible-galaxy install archf.ntpd
```

Basic usage is:

```yaml
- hosts: all
  roles:
    - role: archf.ntpd
```

### Install with git

If you do not want a global installation, clone it into your `roles_path`.

```shell
git clone git@github.com:archf/ansible-ntpd.git /path/to/roles_path
```

But I often add it as a submdule in a given `playbook_dir` repository.

```shell
git submodule add git@github.com:archf/ansible-ntpd.git <playbook_dir>/roles/ntpd
```

As the role is not managed by Ansible Galaxy, you do not have to specify the
github user account.

Basic usage is:

```yaml
- hosts: all
  roles:
  - role: ntpd
```

## Ansible role dependencies

None.

## Todo

  * peer support?
  * improve statistics configuration

## License

BSD.

## Author Information

Felix Archambault.

## Role stack

This role was carefully selected to be part an ultimate deck of roles to manage
your infrastructure.

All roles' documentation is wrapped in this [convenient guide](http://127.0.0.1:8000/).


---
This README was generated using ansidoc. This tool is available on pypi!

```shell
pip3 install ansidoc

# validate by running a dry-run (will output result to stdout)
ansidoc --dry-run <rolepath>

# generate you role readme file
ansidoc <rolepath>
```

You can even use it programatically from sphinx. Check it out.
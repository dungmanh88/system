SSH
===

[![Build Status](https://travis-ci.org/resmo/ansible-role-sshd.png?branch=master)](https://travis-ci.org/resmo/ansible-role-sshd)

This role installs and configures the sshd on their hosts.


Requirements
------------

This role requires Ansible 1.4 or higher, and platform requirements are listed
in the metadata file.


Usage
-----

Example playbook using the defaults:

    - hosts: all
      remote_user: root
      roles:
      - resmo.sshd


2) Install ntp and set some custom settings:

    # file: group_vars/webservers
    ---
    sshd_permit_root_login: without-password

Example playbook:

    - hosts: all
      remote_user: root
      roles:
      - resmo.sshd


License
-------

BSD


Author Information
------------------

- René Moser

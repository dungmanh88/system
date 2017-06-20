FlxPeters.nginx-proxy
=========

[![Build Status](https://travis-ci.org/FlxPeters/ansible-role-nginx-proxy.svg?branch=master)](https://travis-ci.org/FlxPeters/ansible-role-nginx-proxy)

Installs Nginx as reverse proxy on Ubuntu. This role is a wrapper with some defaults for [geerlingguy.nginx](https://github.com/geerlingguy/ansible-role-nginx).

Requirements
------------

The Role is tested for Ubuntu 16.04. 

Role Variables
--------------

`nginx_proxy_pass`: The proxy pass for the Nginx location. Default is `http://localhost:8080` for Tomcat servers.

Dependencies
------------

- geerlingguy:nginx

Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: FlxPeters.nginx-proxy, nginx_proxy_pass: "http://localhost:9000" }

Test
----

This roles uses Molecule to test. You can run the tests like this:

    molecule test
    
The tests are based on Docker and Testinfra.

License
-------

MIT
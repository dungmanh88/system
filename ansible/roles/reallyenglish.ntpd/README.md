# ansible-role-ntpd

Configure ntpd from ntp.org

# Requirements

None

# Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| ntpd\_service | service name | ntpd |
| ntpd\_conf | path to ntp.conf | {{ \_\_ntpd\_conf }} |
| ntpd\_db\_dir | dir to place ntpd.leap-seconds.list | {{ \_\_ntpd\_db\_dir }} |
| ntpd\_leapfile | path to leap-seconds.list | {{ ntpd\_db\_dir }}/leap-seconds.list |
| ntpd\_package | package name | {{ \_\_ntpd\_package }} |
| ntpd\_driftfile | path to `ntp.drift` | {{ \_\_ntpd\_db\_dir }}/ntp.drift |
| ntpd\_leap\_seconds\_url | URL of leap-seconds.list | https://www.ietf.org/timezones/data/leap-seconds.list |
| ntpd\_role | NTP client or server (server is not implemented) | client |
| ntpd\_upstreams | a list of upstream | ["0.pool.ntp.org", "1.pool.ntp.org", "2.pool.ntp.org", "3.pool.ntp.org"] |

## Debian

| Variable | Default |
|----------|---------|
| \_\_ntpd\_service | ntp |
| \_\_ntpd\_conf | /etc/ntp.conf |
| \_\_ntpd\_db\_dir | /var/lib/ntp |
| \_\_ntpd\_package | ntp |

## FreeBSD

| Variable | Default |
|----------|---------|
| \_\_ntpd\_service | ntpd |
| \_\_ntpd\_conf | /etc/ntp.conf |
| \_\_ntpd\_db\_dir | /var/db/ntp |

## RedHat

| Variable | Default |
|----------|---------|
| \_\_ntpd\_service | ntpd |
| \_\_ntpd\_conf | /etc/ntp.conf |
| \_\_ntpd\_db\_dir | /var/lib/ntp |
| \_\_ntpd\_package | ntp |

# Dependencies

None

# Example Playbook

```yaml
- hosts: localhost
  roles:
    - ansible-role-ntpd
```

# License

```
Copyright (c) 2016 Tomoyuki Sakurai <tomoyukis@reallyenglish.com>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```

# Author Information

Tomoyuki Sakurai <tomoyukis@reallyenglish.com>

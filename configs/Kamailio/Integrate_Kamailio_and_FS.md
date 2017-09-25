http://saevolgo.blogspot.com/2012/03/making-rtpproxy-work.html
http://saevolgo.blogspot.com/2013/08/rtpproxy-revisited-kamailio-40.html
http://saevolgo.blogspot.com/2012/06/opensips-as-load-balancer-for.html
http://kb.asipto.com/freeswitch:kamailio-3.0.x-freeswitch-1.0.6d-ms
http://kb.asipto.com/freeswitch:kamailio-3.1.x-freeswitch-1.0.6d-sbc
http://lists.sip-router.org/pipermail/sr-users/2011-September/070196.html
https://lists.kamailio.org//pipermail/sr-users/2011-September/thread.html#70205
https://www.kamailio.org/wiki/cookbooks/4.2.x/pseudovariables
https://www.kamailio.org/wiki/cookbooks/4.4.x/core#mhomed --- If you use private IP for FS you will consider this options
https://www.kamailio.org/docs/modules/5.0.x/modules/rtpproxy.html
https://lists.kamailio.org/pipermail/sr-users/2014-March/082250.html
http://lists.freeswitch.org/pipermail/freeswitch-users/2010-March/055234.html
http://lists.freeswitch.org/pipermail/freeswitch-users/2015-August/115098.html


https://medium.com/southbridge-io/kamailio-sip-proxy-installation-and-minimal-configuration-example-c96b5729853a
https://blog.voipxswitch.com/2015/08/11/rtpengine-with-kamailio-as-load-balancer-and-ip-gateway/
http://www.kamailio.org/events/2010-cluecon/kamailio-cluecon2010.pdf
http://nil.uniza.sk/sip/application-servers/kamailio-configuration-provide-load-balancing-and-failover-media-services
https://blog.voipxswitch.com/2015/03/27/kamailio-basic-sip-proxy-all-requests-setup/#comment-358



Mastering FS ebook
Openser ebook
Opensips ebook
FreeSWITCH 1.2 ebook

Comment:
```
http://saevolgo.blogspot.com/2012/07/freeswitch-with-sip-users-in-mysql-mod.html
Here is my idea:

1- Put in a Kamailio or OpenSIPS infront of your FreeSWITCH Servers, Let the SIP proxy handle the registrations.

2- For any incoming call send call to Load-Balanced array of FreeSWITCH servers who will just do some call routing logic, and if the dialed number matches the extension sequence number route call back to the SIP Proxy.

3- In SIP Proxy detect the call is coming in from the FreeSWITCH servers, try finding the active registered extension in SIP Proxy and connect the call to that user.

4- If in SIP proxy the number is offline, send call to some outbound gateway/trunk.
```

Kamailio:
- load balancer for media servers FS
- SIP registra
- SIP proxy
- SIP auth
- SIP location
- Support RTPProxy module to relay media service
- Two interfaces: WAN and LAN

Media server:
- FS process media service from RTP Proxy
- Only have LAN IP

Architecture

SIP phone A ---> Kamailio(SIP) + rtpproxy(RTP) ---> (FS1,2,3,..,n) ---> Kamailio(SIP) + RTPProxy(RTP) ---> SIP phone B

hostnamectl set-hostname kamailio

Off firewall and selinux

[home_kamailio_v4.3.x-rpms]
name=RPM Packages for Kamailio v4.3.x (RHEL_7)
type=rpm-md
baseurl=http://download.opensuse.org/repositories/home:/kamailio:/v4.3.x-rpms/RHEL_7/
gpgcheck=1
gpgkey=http://download.opensuse.org/repositories/home:/kamailio:/v4.3.x-rpms/RHEL_7//repodata/repomd.xml.key
enabled=1

mkdir -p /var/run/kamailio
chown -R kamailio:kamailio /var/run/kamailio
to save kamailio_fifo and kamailio_ctl...

yum -y install kamailio wget tmux gdb kamailio-mysql kamailio-tls mysql mariadb-server

yum install epel-release
or
wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
rpm -ivh epel-release-latest-7.noarch.rpm

yum install rtpproxy

/etc/kamailio/kamctlrc
```
SIP_DOMAIN=lb-ip
DBENGINE=MYSQL
DBHOST=localhost
DBNAME=kamailio
DBRWUSER="kamailio"
DBRWPW="kamailiorw"
DBACCESSHOST=localhost
DBROOTUSER="root"
```

systemctl restart mariadb && systemctl enable mariadb
systemctl restart kamailio && systemctl enable kamailio

Gen DB
kamdbctl create ### will create db kamailio by default
grant all privileges on `kamailio`.* to 'kamailio'@'localhost' identified by 'kamailiorw';

Start rtpproxy on bridge mode
//rtpproxy -F -l public-lb-ip/private-lb-ip -s udp:127.0.0.1:7722 -d DBUG:LOG_LOCAL0
//rtpproxy -F -l localip -A publicip  -s udp:127.0.0.1:7722 -d DBUG:LOG_LOCAL0

rtpproxy -F -l 103.53.171.121/192.168.171.121 -s udp:127.0.0.1:7722 -d DBUG LOG_LOCAL0

Config kamailio

cd /etc/kamailio
mv kamailio.cfg  kamailio.cfg.orig
cp kamailio-basic.cfg kamailio.cfg

Base on kamailio-basic.cfg
```
# *** To enable mysql:
#     - define WITH_MYSQL
#!define WITH_MYSQL

# *** To enable authentication execute:
#     - enable mysql
#     - define WITH_AUTH
#!define WITH_AUTH

# *** To enable persistent user location execute:
#     - enable mysql
#     - define WITH_USRLOCDB
#!define WITH_USRLOCDB

# *** To enable nat traversal execute:
#     - define WITH_NAT
#!define WITH_NAT
```

- Config global param
```
log_facility=LOG_LOCAL2
mhomed=1

fork=yes
children=4

auto_aliases=no
listen=LISTEN_UDP_PUBLIC:5060
listen=LISTEN_UDP_PRIVATE:5060
```

- Config flag
```
#!define FLAG_FROM_FS 10
#!define FLAG_FROM_PEER 11

sip_warning=no
```

- Config module
```
loadmodule "acc.so"

loadmodule "dispatcher.so"
loadmodule "stun.so"
loadmodule "uac.so"
loadmodule "ipops.so"

#!ifdef WITH_NAT
loadmodule "nathelper.so"
#loadmodule "rtpproxy.so"
loadmodule "rtpengine.so"
#!endif
...
```
- Config param module avpops.so
```
# ----- tm params -----
...
# ----- dispatcher params -----
modparam("dispatcher", "db_url", DBURL)
modparam("dispatcher", "table_name", "dispatcher")
modparam("dispatcher", "flags", 2)
modparam("dispatcher", "dst_avp", "$avp(AVP_DST)")
modparam("dispatcher", "grp_avp", "$avp(AVP_GRP)")
modparam("dispatcher", "cnt_avp", "$avp(AVP_CNT)")
modparam("dispatcher", "sock_avp", "$avp(AVP_SOCK)")
...
# ----- rtpproxy params -----
#modparam("rtpproxy", "rtpproxy_sock", "udp:127.0.0.1:7722")
modparam("rtpengine", "rtpengine_sock", "udp:localhost:22222")
```


- Config routing:
```
request_route {
	# per request initial checks
	route(SANITY_CHECK);

  route(NATDETECT);

	# CANCEL processing
	if (is_method("CANCEL")) {
		if (t_check_trans()) {
			t_relay();
		}
		exit;
	}

  route(REGISTRAR);
  route(AUTH);

	# check src ip and set flag
	route(CHECK_SOURCE_IP);

	# always add record_route when forwarding SUBSCRIBEs
	if (is_method("SUBSCRIBE")) {
		exit;
	}

	# handle requests within SIP dialogs
	route(WITHINDLG);

	### only initial requests (no To tag)
	t_check_trans();

	# dispatch destinations
	route(DISPATCH);
}

route[SANITY_CHECK] {

	if (!mf_process_maxfwd_header("10")) {
		#xlog("L_WARN", "$ci|end|too much hops, not enough barley");
		send_reply("483", "Too Many Hops");
		exit;
	}

	if (!sanity_check()) {
		#xlog("L_WARN", "$ci|end|message is insane");
		exit;
	}

	if ($ua == "friendly-scanner" ||
		$ua == "sundayddr" ||
		$ua =~ "sipcli" ) {
		#xlog("L_WARN", "$ci|end|dropping message with user-agent $ua");
		exit;
	}

}

route[CHECK_SOURCE_IP] {
	if(ds_is_from_list()) {
		setflag(FLAG_FROM_FS);
	} else {
		setflag(FLAG_FROM_PEER);
	}
}

route[RELAY] {

	if (is_method("INVITE")) {
		if(!t_is_set("failure_route")) {
			t_on_failure("MANAGE_FAILURE");
		}
	}

	if (isflagset(FLAG_FROM_PEER)) {
		force_send_socket(LISTEN_UDP_PRIVATE);
 	} else {
		force_send_socket(LISTEN_UDP_PUBLIC);
	}


	if (!t_relay()) {
		sl_reply_error();
	}
	#exit;
}

# Handle requests within SIP dialogs
route[WITHINDLG] {
	if (has_totag()) {
		# sequential request withing a dialog should
		# take the path determined by record-routing
		if (loose_route()) {
			route(RELAY);
		} else {
			if (is_method("NOTIFY")) {
				route(RELAY);
			}

			if (is_method("SUBSCRIBE") && uri == myself) {
				# in-dialog subscribe requests
				exit;
			}

			if (is_method("ACK")) {
				if (t_check_trans()) {
					# non loose-route, but stateful ACK;
					# must be ACK after a 487 or e.g. 404 from upstream server
					t_relay();
					exit;
				} else {
					# ACK without matching transaction ... ignore and discard.
					exit;
				}
			}
			sl_send_reply("404","Not here");
		}
		exit;
	}
}

# Manage failure routing cases
failure_route[MANAGE_FAILURE] {
	if (t_is_canceled()) {
		exit;
	}
}

onreply_route[1] {
	if (has_body("application/sdp")) {
		rtpengine_answer();
	}
}

onreply_route[2] {
	if (has_body("application/sdp")) {
		rtpengine_offer();
	}
}

# Dispatch requests
route[DISPATCH] {
	# round robin dispatching on gateways group '1'
	# record routing for dialog forming requests (in case they are routed)
	# - remove preloaded route headers
	remove_hf("Route");
	if (is_method("INVITE|REFER")) {
		record_route();
		if (has_body("application/sdp")) {
			if (rtpengine_offer()) {
				t_on_reply("1");
			}
		} else {
			t_on_reply("2");
		}
		if (isflagset(FLAG_FROM_PEER)) {
			if(!ds_select_dst("1", "4")) {
				send_reply("404", "No destination");
				exit;
			}
		}
	}

	if (is_method("ACK") && has_body("application/sdp")) {
		rtpengine_answer();
	}
  prefix("kb-");
	route(RELAY);
}

route[REGISTRAR] {
        if (!is_method("REGISTER")) return;
        if(isflagset(FLT_NATS)) {
                setbflag(FLB_NATB);
#!ifdef WITH_NATSIPPING
                # do SIP NAT pinging
                setbflag(FLB_NATSIPPING);
#!endif
        }
        #xlog("test");
        if (!www_authorize("kamailio test", "subscriber")) {
                www_challenge("kamailio test", "0");
                exit;
        }

        if (!save("location"))
                sl_reply_error();

        exit;
}

# Caller NAT detection
route[NATDETECT] {
#!ifdef WITH_NAT
        force_rport();
        if (nat_uac_test("19")) {
                if (is_method("REGISTER")) {
                        fix_nated_register();
                } else {
                        fix_nated_contact();
                }
                setflag(FLT_NATS);
        }
#!endif
        return;
}

route[AUTH] {
#!ifdef WITH_AUTH

#!ifdef WITH_IPAUTH
        if((!is_method("REGISTER")) && allow_source_address()) {
                # source IP allowed
                return;
        }
#!endif

        if(ds_is_from_list("1")) {
                return;
        }

        if (!is_method("REGISTER")) {
                # authenticate requests
                if (!proxy_authorize("kamailio test","subscriber")) {
                        proxy_challenge("kamailio test","0");
                        exit;
                }

                consume_credentials();

        }
        # if caller is not local subscriber, then check if it calls
        # a local destination, otherwise deny, not an open relay here
        if (from_uri!=myself && uri!=myself) {
                sl_send_reply("403","Not relaying");
                exit;
        }

#!endif
        return;
}
```









replace route[REQINIT] to route[SANITY_CHECK]
```
# per request initial checks
#route(REQINIT);
route(SANITY_CHECK);

route[SANITY_CHECK] {
        if (!mf_process_maxfwd_header("10")) {
                #xlog("L_WARN", "$ci|end|too much hops, not enough barley");
                send_reply("483", "Too Many Hops");
                exit;
        }

        if (!sanity_check()) {
                #xlog("L_WARN", "$ci|end|message is insane");
                exit;
        }

        if ($ua == "friendly-scanner" ||
                $ua == "sundayddr" ||
                $ua =~ "sipcli" ) {
                #xlog("L_WARN", "$ci|end|dropping message with user-agent $ua");
                exit;
        }
}

```

- Block scanner
```
if($ua =~ "friendly-scanner") {
        sl_send_reply("404", "NOt here");
        exit;
}
```
- Rewrite auth in registra and invite process
```
# Handle SIP registrations
route[REGISTRAR] {
        if (!is_method("REGISTER")) return;
        if(isflagset(FLT_NATS)) {
                setbflag(FLB_NATB);
#!ifdef WITH_NATSIPPING
                # do SIP NAT pinging
                setbflag(FLB_NATSIPPING);
#!endif
        }
        #xlog("test");
        if (!www_authorize("kamailio test", "subscriber")) {
                www_challenge("kamailio test", "0");
                exit;
        }

        if (!save("location"))
                sl_reply_error();

        exit;
}

# IP authorization and user uthentication
route[AUTH] {
#!ifdef WITH_AUTH

#!ifdef WITH_IPAUTH
        if((!is_method("REGISTER")) && allow_source_address()) {
                # source IP allowed
                return;
        }
#!endif

        if(ds_is_from_list("1")) {
                return;
        }

        if (!is_method("REGISTER")) {
                # authenticate requests
                if (!proxy_authorize("kamailio test","subscriber")) {
                        proxy_challenge("kamailio test","0");
                        exit;
                }

                consume_credentials();

        }
        # if caller is not local subscriber, then check if it calls
        # a local destination, otherwise deny, not an open relay here
        if (from_uri!=myself && uri!=myself) {
                sl_send_reply("403","Not relaying");
                exit;
        }

#!endif
        return;
}
```
- Request route
```
if ($rU==$null) {
        # request with no Username in RURI
        sl_send_reply("484","Address Incomplete");
        exit;
}

route(DISPATCH);

# user location service
route(LOCATION);
```
- route[DISPATCH]
```
route[DISPATCH] {

        if(!is_method("INVITE")){
                return;
        }

        if(ds_is_from_list("1")) {
                return;
        }

        prefix("kb-");
        # round robin dispatching on gateways group '1'
        if(!ds_select_dst("1", "4"))
        {
                send_reply("404", "No destination");
                exit;
        }
        xlog("L_DBG", "--- SCRIPT: going to <$ru> via <$du>\n");
        t_on_failure("RTF_DISPATCH");
        route(RELAY);
        exit;
}
```
- failure_route[RTF_DISPATCH]
```
# Sample failure route
failure_route[RTF_DISPATCH] {
        if (t_is_canceled()) {
                exit;
        }
        # next DST - only for 500 or local timeout
        if (t_check_status("500")
                        or (t_branch_timeout() and !t_branch_replied()))
        {
                if(ds_next_dst())
                {
                        t_on_failure("RTF_DISPATCH");
                        route(RELAY);
                        exit;
                }
        }
}
```
- Rewrite route[NATMANAGE]
```
if (!(isflagset(FLT_NATS) || isbflagset(FLB_NATB)))
        return;

if (is_method("BYE")) {
        xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in Route[RTPPROXY] unforced RTP Proxy STATS='$rtpstat'\n");
        rtpproxy_destroy();
} else if (is_method("INVITE")) {
        if(avp_db_query("select destination from dispatcher where destination like '%$dd%'")){
                xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in route[RTPPROXY] RTPproxy with IE Flags\n");
                rtpproxy_manage("rwei");

        }
        else if(avp_db_query("select destination from dispatcher where destination='sip:$si:$sp'")){
                 xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in route[RTPPROXY] RTPproxy with EI Flags\n");
                rtpproxy_manage("rwie");

        }
        else {
                xlog("L_NOTICE","$rm from $fu (IP:$si:$sp) in Route[RTPPROXY] Forcing RTPproxy\n");
          #      rtpproxy_manage("r");
        }
}

#rtpproxy_manage("co");
```

- Add db of kamailio
insert into dispatcher(setid, destination) values(1,'sip:fs-ip-1|2:5060');
```
mysql> select * from dispatcher\G
*************************** 1. row ***************************
         id: 1
      setid: 1
destination: sip:fs-ip-1:5060
      flags: 0
   priority: 0
      attrs:
description:
*************************** 2. row ***************************
         id: 2
      setid: 1
destination: sip:fs-ip-2:5060
      flags: 0
   priority: 0
      attrs:
description:
2 rows in set (0.00 sec)
```

kamailio -c -f kamailio.cfg
```
oading modules under config path: /usr/lib64/kamailio/modules/
 0(6505) INFO: <core> [sctp_core.c:75]: sctp_core_check_support(): SCTP API not enabled - if you want to use it, load sctp module
Listening on
             udp: 127.0.0.1:5060
             udp: 172.31.21.142:5060
             tcp: 127.0.0.1:5060
             tcp: 172.31.21.142:5060
Aliases:
             *: 54.202.25.215:*

config file ok, exiting...
```

On Freeswitch
- Follow Install_from_pkgs.md to install Freeswitch
- Follow Acl instruction
- Some dialplan
/etc/freeswitch/dialplan/public.xml
```
<include>
  <context name="public">


  <extension name="from_kamailio">
      <condition field="network_addr" expression="^xx\.xx\.xx\.xx$" /> // this is IP of kamailio
      <condition field="destination_number" expression="^(.+)$">
        <action application="transfer" data="$1 XML default"/>
      </condition>
    </extension>

```
/etc/freeswitch/dialplan/default.xml
```
<extension name="extension-intercom">
...
<!--
     dial the extension (1000-1019) for 30 seconds and go to voicemail if the
     call fails (continue_on_fail=true), otherwise hang up after a successful
     bridge (hangup_after_bridge=true)
-->

<extension name="kbridge">
  <condition field="destination_number" expression="^kb-(.+)$">
              <action application="set" data="proxy_media=true"/>
              <action application="set" data="call_timeout=50"/>
              <action application="set" data="continue_on_fail=true"/>
              <action application="set" data="hangup_after_bridge=true"/>
              <action application="set" data="sip_invite_domain=fs-ip"/> // this is ip of fs
              <action application="export" data="sip_contact_user=ufs"/>
              <action application="bridge" data="sofia/$${domain}/$1@lb-ip"/> // this is ip of kamailio
              <action application="answer"/>
            <!--  <action application="voicemail" data="default ${domain_name} $1"/> -->
  </condition>
</extension>
<extension name="Local_Extension">
...
```
config /etc/rsyslog.conf
```
local2.*                        -/var/log/kamailio.log
```

You don't need config user directory on FS, you don't need sync directory data between FS servers

restart kamailio and FS service, rsyslog

TEST
Add some sip on kamailio
kamctl add 8888 8888
kamctl add 9999 9999

register two sip phone with domain lb-ip

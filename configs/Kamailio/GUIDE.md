https://beingasysadmin.wordpress.com/2014/02/23/integrating-kamailio-with-freeswitch/
http://kb.asipto.com/freeswitch:kamailio-3.3.x-freeswitch-1.2.x-sbc
http://kamailio.org/docs/modules/4.3.x/modules/dispatcher.html#idp51012572

[home_kamailio_v4.3.x-rpms]
name=RPM Packages for Kamailio v4.3.x (RHEL_7)
type=rpm-md
baseurl=http://download.opensuse.org/repositories/home:/kamailio:/v4.3.x-rpms/RHEL_7/
gpgcheck=1
gpgkey=http://download.opensuse.org/repositories/home:/kamailio:/v4.3.x-rpms/RHEL_7//repodata/repomd.xml.key
enabled=1


yum install kamailio

yum install kamailio-mysql kamailio-tls

insert into dispatcher(setid, destination) values(1,'sip:lb-ip:5080');


/etc/kamailio/kamailio.cfg
```
#!define WITH_MYSQL
#!define WITH_AUTH
#!define WITH_USRLOCDB
#!define WITH_FREESWITCH
log_facility=LOG_LOCAL2
listen=udp:lb-ip:5060
port=5060

####### Custom Parameters #########
#!ifdef WITH_FREESWITCH
freeswitch.bindip = "fs-ip" desc "FreeSWITCH IP Address"
freeswitch.bindport = "5060" desc "FreeSWITCH Port"
#!endif

####### Modules Section ########
loadmodule "dispatcher.so"


####### Routing Logic ########


# Main SIP request routing logic
# - processing of any incoming SIP request starts with this route
# - note: this is the same as route { ... }
request_route {
...
if ($rU==$null) {
        # request with no Username in RURI
        sl_send_reply("484","Address Incomplete");
        exit;
}


route(DISPATCH);

# dispatch destinations to PSTN
#route(PSTN);

#!ifdef WITH_FREESWITCH
# save callee ID
#$avp(callee) = $rU;
#route(FSDISPATCH);
#!endif

# user location service
#route(LOCATION);

#route(RELAY);
}


route[DISPATCH] {
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


#!ifdef WITH_FREESWITCH
# FreeSWITCH routing blocks
route[FSINBOUND] {
        if($si== $sel(cfg_get.freeswitch.bindip)
                        && $sp==$sel(cfg_get.freeswitch.bindport))
                return 1;
        return -1;
}

route[FSDISPATCH] {
        if(!is_method("INVITE"))
                return;
        if(route(FSINBOUND))
                return;

        # dial number selection
        switch($rU) {
                case /"^41$":
                        # 41 - voicebox menu
                        # allow only authenticated users
                        if($au==$null)
                        {
                                sl_send_reply("403", "Not allowed");
                                exit;
                        }
                        $rU = "vm-" + $au;
                break;
                case /"^441[0-9][0-9]$":
                        # starting with 44 folowed by 1XY - direct call to voice box
                        strip(2);
                        route(FSVBOX);
                break;
                case /"^433[01][0-9][0-9]$":
                        # starting with 433 folowed by (0|1)XY - conference
                        strip(2);
                break;
                case /"^45[0-9]+$":
                        strip(2);
                break;
                default:
                        # offline - send to voicebox
                        if (!registered("location"))
                        {
                                route(FSVBOX);
                                exit;
                        }
                        # online - do bridging
                        prefix("kb-");
                        if(is_method("INVITE"))
                        {
                                # in case of failure - re-route to FreeSWITCH VoiceMail
                                t_on_failure("FAIL_FSVBOX");
                              }
              }
              route(FSRELAY);
              exit;
      }

route[FSVBOX] {
        if(!($rU=~"^1[0-9][0-9]+$"))
                return;
        prefix("vb-");
        route(FSRELAY);
}

route[FSRELAY] {
        $du = "sip:" + $sel(cfg_get.freeswitch.bindip) + ":" + $sel(cfg_get.freeswitch.bindport);
        if($var(newbranch)==1)
        {
                append_branch();
                $var(newbranch) = 0;
        }
        route(RELAY);
        exit;
}


#!ifdef WITH_FREESWITCH
failure_route[FAIL_FSVBOX] {
#!ifdef WITH_NAT
        if (is_method("INVITE")
                        && (isbflagset(FLB_NATB) || isflagset(FLT_NATS))) {
                unforce_rtp_proxy();
        }
#!endif

        if (t_is_canceled()) {
                exit;
        }

        if (t_check_status("486|408")) {
                # re-route to FreeSWITCH VoiceMail
                $rU = $avp(callee);
                route(FSVBOX);
        }
}
#!endif

```

/etc/freeswitch/vars.xml
```
<!-- Internal SIP Profile -->
<X-PRE-PROCESS cmd="set" data="internal_auth_calls=false"/>
<X-PRE-PROCESS cmd="set" data="internal_sip_port=5060"/>
<X-PRE-PROCESS cmd="set" data="internal_tls_port=5061"/>
<X-PRE-PROCESS cmd="set" data="internal_ssl_enable=false"/>

<!-- External SIP Profile -->
<X-PRE-PROCESS cmd="set" data="external_auth_calls=false"/>
<X-PRE-PROCESS cmd="set" data="external_sip_port=5080"/>
<X-PRE-PROCESS cmd="set" data="external_tls_port=5081"/>
<X-PRE-PROCESS cmd="set" data="external_ssl_enable=false"/>
```

/etc/freeswitch/dialplan/public.xml
```
<include>
  <context name="public">


  <extension name="from_kamailio">
      <condition field="network_addr" expression="^xx\.xx\.xx\.xx$" />
      <condition field="destination_number" expression="^(.+)$">
        <action application="transfer" data="$1 XML default"/>
      </condition>
    </extension>

```

/etc/freeswitch/autoload_configs/acl.conf.xml
```
<list name="domains" default="deny">
  <!-- domain= is special it scans the domain from the directory to build the ACL -->
  <node type="allow" domain="$${domain}"/>
  <!-- use cidr= if you wish to allow ip ranges to this domains acl. -->
  <!-- <node type="allow" cidr="192.168.0.0/24"/> -->
  <node type="allow" cidr="xx.xx.xx.0/24"/>
</list>
```

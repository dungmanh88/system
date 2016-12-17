#!/bin/bash

set -e
export MASTER_HOST=192.168.14.11
export MINION_IP=192.168.14.51
export MINION_HOST=minion4
export WORKER_IP=${MINION_IP}
export WORKER_FQDN=${MINION_HOST}
export NETWORK_PLUGIN=""

export ETCD_ENDPOINTS=http://192.168.14.11:2379
export WORKER_PUBLIC_IP=${MINION_IP}
export WORKER_ADVERTISE_IP=${MINION_IP}

export K8S_SERVICE_IP=10.3.0.1
export DNS_SERVICE_IP=10.3.0.10
export K8S_VER=v1.4.5_coreos.0

export ca_pem_file=/tmp/ca.pem
export ca_key_pem_file=/tmp/ca-key.pem
export ca_srl_file=/tmp/ca.srl

export kube_config_dir=/etc/kubernetes
export openssl_dir=/etc/kubernetes/ssl
export flannel_config_dir=/etc/flannel
export system_service_dir=/etc/systemd/system
export manifest_path=${kube_config_dir}/manifests
export flannel_service_dir=${system_service_dir}/flanneld.service.d

export PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

function change_minion_hostname() {
  echo "CHANGE MINION HOSTNAME"
  hostnamectl set-hostname $MINION_HOST
  echo "${MINION_IP} ${MINION_HOST}" >> /etc/hosts
  echo "127.0.0.1 ${MINION_HOST}" >> /etc/hosts
  echo "CHANGE MINION HOSTNAME DONE!!!"
}

function enable_timedatectl() {
  echo "ENABLE TIMEDATECTL"
  timedatectl set-timezone UTC
  timedatectl set-timezone Asia/Ho_Chi_Minh
  systemctl start systemd-timesyncd
  systemctl enable systemd-timesyncd
  systemctl stop ntpd
  systemctl disable ntpd
  echo "ENABLE TIMEDATECTL DONE!!!"
}

function disable_selinux() {
  echo "DISABLE SELINUX"
  setenforce 0
  echo "DISABLE SELINUX DONE!!!"
}

function disable_firewall() {
  echo "DISABLE FIREWALL"
  iptables -F
  iptables -t nat -F
  systemctl disable iptables
  echo "DISABLE FIREWALL DONE!!!"
}

function create_kube_dir() {
  echo "CREATE KUBE DIR"
  mkdir -p ${openssl_dir}
  mkdir -p ${kube_config_dir}
  cp ${ca_pem_file} ${openssl_dir}/ca.pem
  cp ${ca_srl_file} ${openssl_dir}/ca.srl
  cp ${ca_key_pem_file} ${openssl_dir}/ca-key.pem
  echo "CREATE KUBE DIR DONE!!!"
}

function install_certificate() {
  echo "INSTALL CERTIFICATE"
  local openssl_cnf=${openssl_dir}/worker-openssl.cnf
  if [ ! -f ${openssl_cnf} ]; then
    echo "create openssl_cnf: ${openssl_cnf}"
    cat << EOF > ${openssl_cnf}
[req]
req_extensions = v3_req
distinguished_name = req_distinguished_name
[req_distinguished_name]
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names
[alt_names]
IP.1 = ${WORKER_IP}
EOF
  fi
  openssl genrsa -out ${openssl_dir}/${WORKER_FQDN}-worker-key.pem 2048
  openssl req -new -key ${openssl_dir}/${WORKER_FQDN}-worker-key.pem -out ${openssl_dir}/${WORKER_FQDN}-worker.csr -subj "/CN=${WORKER_FQDN}" -config ${openssl_cnf}
  openssl x509 -req -in ${WORKER_FQDN}-worker.csr -CA ${openssl_dir}/ca.pem -CAkey ${openssl_dir}/ca-key.pem -CAcreateserial -out ${openssl_dir}/${WORKER_FQDN}-worker.pem -days 365 -extensions v3_req -extfile ${openssl_dir}/worker-openssl.cnf
  echo "create worker.pem"
  ln -s ${openssl_dir}/${WORKER_FQDN}-worker.pem ${openssl_dir}/worker.pem
  echo "create worker-key.pem"
  ln -s ${openssl_dir}/${WORKER_FQDN}-worker-key.pem ${openssl_dir}/worker-key.pem
  chmod 600 ${openssl_dir}/*-key.pem
  chown root:root ${openssl_dir}/*-key.pem
  echo "INSTALL CERTIFICATE DONE!!!"
}

function install_flannel() {
  echo "INSTALL FLANNEL"
  mkdir -p ${flannel_config_dir}
  local flannel_cnf=${flannel_config_dir}/options.env
  if [ ! -f ${flannel_cnf} ]; then
    echo "create flannel_cnf: ${flannel_cnf}"
    cat << EOF > ${flannel_cnf}
FLANNELD_IFACE=${WORKER_ADVERTISE_IP}
FLANNELD_ETCD_ENDPOINTS=${ETCD_ENDPOINTS}
EOF
  fi
  mkdir -p ${flannel_service_dir}
  local flannel_service_cnf=${flannel_service_dir}/40-ExecStartPre-symlink.conf
  if [ ! -f ${flannel_service_cnf} ]; then
    echo "create flannel_service_cnf: ${flannel_service_cnf}"
    cat << EOF > ${flannel_service_cnf}    
[Service]
ExecStartPre=/usr/bin/ln -sf ${flannel_cnf} /run/flannel/options.env
mkdir -p /etc/systemd/system/docker.service.d
vi /etc/systemd/system/docker.service.d/40-flannel.conf
[Unit]
Requires=flanneld.service
After=flanneld.service
EOF
  fi
  echo "INSTALL FLANNEL DONE!!!"
}

function install_kubelet() {
  echo "INSTALL KUBELET"
  local kubelet_service_cnf=${system_service_dir}/kubelet.service
  if [ ! -f ${kubelet_service_cnf} ]; then
    echo "create kubelet_service_cnf: ${kubelet_service_cnf}"
    cat << EOF > ${kubelet_service_cnf}    
[Service]
ExecStartPre=/usr/bin/mkdir -p /etc/kubernetes/manifests
ExecStartPre=/usr/bin/mkdir -p /var/log/containers

Environment=KUBELET_VERSION=${K8S_VER}
Environment="RKT_OPTS=--volume var-log,kind=host,source=/var/log \
  --mount volume=var-log,target=/var/log \
  --volume dns,kind=host,source=/etc/resolv.conf \
  --mount volume=dns,target=/etc/resolv.conf"

ExecStart=/usr/lib/coreos/kubelet-wrapper \
  --api-servers=https://${MASTER_HOST} \
  --network-plugin-dir=/etc/kubernetes/cni/net.d \
  --network-plugin=${NETWORK_PLUGIN}  \
  --register-node=true \
  --allow-privileged=true \
  --config=/etc/kubernetes/manifests \
  --hostname-override=${WORKER_ADVERTISE_IP} \
  --cluster-dns=${DNS_SERVICE_IP} \
  --cluster-domain=cluster.local \
  --kubeconfig=/etc/kubernetes/worker-kubeconfig.yaml \
  --tls-cert-file=/etc/kubernetes/ssl/worker.pem \
  --tls-private-key-file=/etc/kubernetes/ssl/worker-key.pem
Restart=always
RestartSec=10
[Install]
WantedBy=multi-user.target
EOF
  fi
  echo "INSTALL KUBELET DONE!!!"
}

function install_kube_proxy() {
  echo "INSTALL KUBE PROXY"
  mkdir -p ${manifest_path}
  local kube_proxy_cnf=${manifest_path}/kube-proxy.yaml
  if [ ! -f ${kube_proxy_cnf} ]; then
    echo "create kube_proxy_cnf: ${kube_proxy_cnf}"
    cat << EOF > ${kube_proxy_cnf}    
apiVersion: v1
kind: Pod
metadata:
  name: kube-proxy
  namespace: kube-system
spec:
  hostNetwork: true
  containers:
  - name: kube-proxy
    image: quay.io/coreos/hyperkube:v1.4.5_coreos.0
    command:
    - /hyperkube
    - proxy
    - --master=https://103.53.171.210
    - --kubeconfig=/etc/kubernetes/worker-kubeconfig.yaml
    - --proxy-mode=iptables
    securityContext:
      privileged: true
    volumeMounts:
      - mountPath: /etc/ssl/certs
        name: "ssl-certs"
      - mountPath: /etc/kubernetes/worker-kubeconfig.yaml
        name: "kubeconfig"
        readOnly: true
      - mountPath: /etc/kubernetes/ssl
        name: "etc-kube-ssl"
        readOnly: true
  volumes:
    - name: "ssl-certs"
      hostPath:
        path: "/usr/share/ca-certificates"
    - name: "kubeconfig"
      hostPath:
        path: "/etc/kubernetes/worker-kubeconfig.yaml"
    - name: "etc-kube-ssl"
      hostPath:
        path: "/etc/kubernetes/ssl"    
EOF
  fi
  echo "INSTALL KUBE PROXY DONE!!!"
}

function install_kube_config() {
  echo "INSTALL KUBE CONFIG"
  local kube_cnf=${kube_config_dir}/worker-kubeconfig.yaml
  if [ ! -f ${kube_cnf} ]; then
    echo "create kube_cnf: ${kube_cnf}"
    cat << EOF > ${kube_cnf}      
apiVersion: v1
kind: Config
clusters:
- name: local
  cluster:
    certificate-authority: /etc/kubernetes/ssl/ca.pem
users:
- name: kubelet
  user:
    client-certificate: /etc/kubernetes/ssl/worker.pem
    client-key: /etc/kubernetes/ssl/worker-key.pem
contexts:
- context:
    cluster: local
    user: kubelet
  name: kubelet-context
current-context: kubelet-context
EOF
  fi
  echo "INSTALL KUBE CONFIG DONE!!!"
}

function start_service_all() {
  for SERVICES in flanneld kubelet; do 
    systemctl daemon-reload
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES 
  done
}

function main() {
  change_minion_hostname \
  && enable_timedatectl \
  && disable_selinux \
  && disable_firewall \
  && create_kube_dir \
  && install_certificate \
  && install_flannel \
  && install_kubelet \
  && install_kube_proxy \
  && install_kube_config \
  && start_service_all
  echo "PLEASE REBOOT MACHINE AFTER COMPLETING THIS SCRIPT"
}

main

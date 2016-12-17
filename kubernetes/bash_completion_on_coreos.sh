#!/bin/bash

set -e

toolbox dnf -y install bash-completion wget \
  && toolbox wget https://raw.githubusercontent.com/docker/docker/master/contrib/completion/bash/docker -O /usr/share/bash-completion/completions/docker \
  && toolbox cp -r /usr/share/bash-completion /media/root/var/
  
echo "export PATH=$PATH:/opt/bin/" >> ~/.bashrc
source /var/bash-completion/bash_completion
echo "source /var/bash-completion/bash_completion" >> ~/.bashrc
source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc

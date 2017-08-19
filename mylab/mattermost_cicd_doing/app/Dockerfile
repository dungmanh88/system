FROM golang
ENV PATH /opt/mattermost/bin:$PATH

RUN apt-get -y update && apt-get -y install netcat jq libpng-dev build-essential zip \
  && curl -sL https://deb.nodesource.com/setup_6.x | bash - \
  && apt-get install -y nodejs \
  && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
  && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
  && apt-get update && apt-get install -y yarn \
  && mkdir -p $GOPATH/src/github.com/mattermost/platform

COPY code/ $GOPATH/src/github.com/mattermost/platform

RUN cd $GOPATH/src/github.com/mattermost/platform \
  && make clean \
  && make build-linux \
  && make package \
  && cd $GOPATH/src/github.com/mattermost/platform/dist \
  && cp -r $GOPATH/src/github.com/mattermost/platform/dist/mattermost /opt \
  && mkdir -p /opt/mattermost/data \
  && useradd --system --user-group mattermost \
  && chown -R mattermost:mattermost /opt/mattermost \
  && chmod -R g+w /opt/mattermost

RUN apt-get autoremove -y libpng-dev build-essential zip nodejs yarn npm

COPY docker-entry.sh /
RUN chmod +x /docker-entry.sh
ENTRYPOINT ["/docker-entry.sh"]

EXPOSE 8065
VOLUME /opt/mattermost/data
VOLUME /opt/mattermost/bin/
WORKDIR /opt/mattermost/bin
#USER mattermost
CMD ["platform"]

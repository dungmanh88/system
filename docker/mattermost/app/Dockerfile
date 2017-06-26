FROM centos:7
LABEL maintainer "dungnm@mm.swat.example.com"
ENV PATH /opt/mattermost/bin:$PATH

# need mattermost after make packages in here to copy
COPY code/ /opt/mattermost

RUN yum -y install wget curl nc \
  && wget -O /tmp/jq https://github.com/stedolan/jq/releases/download/jq-1.5/jq-linux64 \
  && chmod +x /tmp/jq \
  && cp /tmp/jq /usr/bin \
  && mkdir -p /opt/mattermost/data \
  && useradd --system --user-group mattermost \
  && chown -R mattermost:mattermost /opt/mattermost \
  && chmod -R g+w /opt/mattermost

COPY docker-entry.sh /
RUN chmod +x /docker-entry.sh
ENTRYPOINT ["/docker-entry.sh"]

EXPOSE 8065
VOLUME /opt/mattermost/data
VOLUME /opt/mattermost/bin/
WORKDIR /opt/mattermost/bin
USER mattermost
CMD ["platform"]

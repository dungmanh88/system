FROM centos:7
LABEL maintainer "dungnm@nal.vn"
ENV PATH /opt/mattermost/bin:$PATH

# need mattermost after make packages in here to copy
COPY mattermost/ /opt/mattermost

RUN mkdir -p /opt/mattermost/data \
  && useradd --system --user-group mattermost \
  && chown -R mattermost:mattermost /opt/mattermost \
  && chmod -R g+w /opt/mattermost

USER mattermost
VOLUME /opt/mattermost/data
WORKDIR /opt/mattermost/bin
CMD ["platform"]

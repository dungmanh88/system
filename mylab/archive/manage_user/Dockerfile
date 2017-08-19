FROM centos:latest

RUN yum -y install epel-release \
        && yum -y install python34 python-pip mysql-devel python-devel gcc gcc-c++ \
 	&& pip install --upgrade pip \
	&& pip install flask MySQL-python

COPY ./ /app
WORKDIR /app
EXPOSE 5000
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "user.py"]

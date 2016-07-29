FROM centos:latest

RUN yum -y install epel-release \
        && yum -y install python34 python-pip python-devel gcc gcc-c++ \
 	&& pip install --upgrade pip \
	&& pip install flask uwsgi

COPY ./ /simple_flask
WORKDIR /simple_flask

CMD ["uwsgi", "--ini", "wsgi.ini"]

FROM centos:latest

RUN yum -y install epel-release \
        && yum -y install python34 python-pip mysql-devel python-devel gcc gcc-c++ \
 	&& pip install --upgrade pip \
	&& pip install flask

COPY ./ /app
WORKDIR /app
EXPOSE 5000

CMD ["python", "simple_flask.py"]

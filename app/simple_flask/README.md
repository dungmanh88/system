### Docker

docker network create my-net
cd system/app/simple_flask/code
docker build -t xavivn/simple_flask .
docker run -itd --net=my-net --name=simpleflask_app_1 xavivn/simple_flask:latest
docker run -itd --net=my-net --name=simpleflask_web_1 -p 80:80 -v ./web/nginx/simple_flask.conf:/etc/nginx/conf.d/simple_flask.conf nginx

### Use Docker compose
docker-compose up

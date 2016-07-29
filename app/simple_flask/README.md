### Docker

docker network create my-net
cd system/app/simple_flask/
docker build -t xavivn/simple_flask code/
docker run -itd --net=my-net --name=simpleflask_app_1 xavivn/simple_flask:latest
mkdir -p /app/simple_flask/web/nginx/
cp web/nginx/simple_flask.conf /app/simple_flask/web/nginx/
docker run -itd --net=my-net --name=simpleflask_web_1 -p 80:80 -v /app/simple_flask/web/nginx/simple_flask.conf:/etc/nginx/conf.d/simple_flask.conf nginx

### Use Docker compose
docker-compose up

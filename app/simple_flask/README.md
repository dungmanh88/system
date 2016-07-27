### Docker

docker network create my-net
cd system/app/simple_flask
docker build -t xavivn/simple_flask .
docker run -itd --net=my-net --name=nginx -v /app/simple_flask/nginx/simple_flask.conf:/etc/nginx/conf.d/simple_flask.conf nginx
docker run -it --net=my-net --name=simple_flask -p 9000:9000 xavivn/simple_flask:latest

### Docker

docker network create my-net
cd system/app/simple_flask
docker build -t xavivn/simple_flask .
docker run -it --net=my-net --name=simple_flask -p 8000:8000 xavivn/simple_flask:latest
docker run -itd --net=my-net --name=nginx -p 80:80 -v /app/simple_flask/nginx/simple_flask.conf:/etc/nginx/conf.d/simple_flask.conf nginx

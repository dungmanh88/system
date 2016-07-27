### Docker

docker network create my-net
cd system/app/simple_flask
docker build -t xavivn/simple_flask .
docker run -it --net=my-net --name=simple_flask -p 5000:5000 xavivn/simple_flask:latest


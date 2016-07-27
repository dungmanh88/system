docker network create my-net

docker run -itd --net=my-net  --name=db -e MYSQL_ROOT_PASSWORD=password mysql:5.6
docker run -it --net=my-net --name=app -p 5000:5000 -e HOST=db -e USER=root -e PASSWORD=password -e DB=test xavivn/manage_user:latest

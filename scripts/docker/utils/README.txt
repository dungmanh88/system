docker build -t my-util -f docker-util  .
docker run -itd --name test my-util
docker exec -it test sh

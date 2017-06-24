```
docker pull <img>
docker run -itd <img_name> <cmd>
docker run -it <img_name> <cmd>
docker exec -it <container_name> <cmd>

<cmd> := sh|bash
```

# Build image
```
docker build -t test .
```

# Manage container
```
docker ps | grep nginx | awk '{ print $1 }' | xargs docker rm -f
```
```
docker ps -a | grep -v Up | grep -v "CONTAINER" | awk '{print $1}' | xargs docker rm -f
```
```
docker run --rm -v /foo -v awesome:/bar busybox top
```
--rm will remove container and anonymous volume (/foo) but not the /bar when it exits.

```
docker run -itd --name some-app --link <container_name>:<alias> <image>

eg:
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
docker run --name some-app --link some-mysql:some-mysql -itd alpine
```

# Manage docker image
```
docker rmi img_name
```
## Remove dangling image
```
docker rmi $(docker images -f dangling=true -q)
```

# Manage volume
```
docker volume ls
```
## Remove dangling volume
```
docker volume rm $(docker volume ls -f dangling=true -q)
```

# Docker swarm manager node

## Create swarm
```
docker swarm init --advertise-addr <PUBLIC MANAGER IP>
docker info
docker node ls
docker swarm join-token worker
```

## Manage service

### Create service
```
docker service create --replicas 1 --name <service-name> <image-name> <command within container>
```

### Publish port for service
```
docker service create \
  --name <service-name> \
  --publish <PUBLISHED-PORT>:<TARGET-PORT> \
  --replicas 2 \
  <image>

PUBLISHED-PORT = NODE-PORT-IN-K8S

docker service update \
--publish-add <PUBLISHED-PORT>:<TARGET-PORT> \
  <SERVICE>

publish add will add more publish port and will not remove old publish port.
```

### List service
```
docker service ls
```

### Inspect service
```
docker service inspect --pretty <service-name>
docker service inspect <service-name>
```

### Inspect node
```
docker node inspect --pretty <node-name-in-docker-node-ls-output>
```

### Which node is running service
```
docker service ps <service-name>
```

### Scale
```
docker service scale <service-name>=<number of scale>
```

### Delete service
```
docker service rm <service-name>
```

### Make node as drain
```
docker node update --availability drain <node-name-in-docker-node-ls-output>
```

### List node
```
docker node ls
```

## Deploy docker compose
```
docker stack deploy --compose-file docker-compose.yml lab
```

# Docker swarm worker node
```
docker swarm join \
   --token xxx \
   <PUBLIC MANAGER IP>:2377
```

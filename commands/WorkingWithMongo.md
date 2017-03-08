```
mongo --port <port> -u admin -p <pass> --authenticationDatabase admin
mongo --port <port> -u root -p <pass> --authenticationDatabase admin
mongo --port <port> -u dumper -p <pass> --authenticationDatabase admin
```

```
use test123
db.createUser(
  {
    user: "test123",
    pwd: "pass",
    roles: [ { role: "dbAdmin", db: "test123" }, { role: "readWrite", db: "test123" } ]
  }
)
```

```
db.getUsers()
[
        {
                "_id" : "test123.test123",
                "user" : "test123",
                "db" : "test123",
                "roles" : [
                        {
                                "role" : "dbAdmin",
                                "db" : "test123"
                        },
                        {
                                "role" : "readWrite",
                                "db" : "test123"
                        }
                ]
        }
]
```
Note: user create follow db

```
use test123
db.dropUser("test123")
```

```
db
show dbs
```

# Group management
## Get group of current user
```
groups
id
```

## Get group of other user
```
groups username
id username
```

## Create group
```
groupadd foo
```

## Check group
```
cat /etc/group
```

## Get all members of a group
https://www.cyberciti.biz/faq/linux-list-all-members-of-a-group/
```
lid -g groupname
or
cat /etc/group | grep groupname
```

## Remove member from all secondary groups
```
usermod -G "" username
```

# User management
## Check user
```
cat /etc/passwd | grep username
```

## Create user
```
useradd username
```

## Set passwd for user
```
passwd username
```

https://www.cyberciti.biz/faq/ubuntu-add-user-to-group/
## Add user to group
```
usermod -a -G groupname username
```
eg:
```
groups test
test : test admins -> test is primary group, admins is secondary group
```

## Change primary group of user
```
usermod -g groupname username
```
eg:
```
group test
test : admins -> adnins become to primary group
```

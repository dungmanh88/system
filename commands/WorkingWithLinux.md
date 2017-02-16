## SSH
### Copy public key
```
ssh-copy-id -i /path/to/public-key user@host
```

### Use key to commit code
If private key name is different
```
ssh-add ~/.ssh/id_rsa_xxx
git add -A; git commit -m "Add"; git push  -u origin master
git pull
```
or
```
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa_xxx; git add -A; git commit -m "Add"; git push  -u origin master'
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa_xxx; git pull'
```

## File
### Delete file in a path
```
find . -iname "*retry*" | xargs rm -f
```

### Check differences
Follow: https://askubuntu.com/questions/111495/how-to-diff-multiple-files-across-directories
```
diff -r dir1/ dir2/
```

### Create softlink
```
ln -s /path/to/origin/dir /path/to/symlink
```

### Sort file/dir by modification time
```
ls -lt /path/to/dir ### order by asc
ls -ltr /path/to/dir ### order by desc
```

### Remove folder order than a specific day
https://unix.stackexchange.com/questions/92346/why-does-find-mtime-1-only-return-files-older-than-2-days
```
base_output=/data/local-backup
find ${base_output} -type d | xargs rmdir > /dev/null ### remove empty dir, redirect if rm non empty dir
find ${base_output} -mtime +1 | xargs rm -rf ### rm files whose age is order than 2 days -> Keep files whose age less than 2 days
```

### Encrypt files
https://askubuntu.com/questions/17641/create-encrypted-password-protected-zip-file
```
zip --encrypt file.zip files ### enter pass to zip
unzip file.zip ### enter pass to unzip
```

## User Group management

### Group management
#### Get group of current user
```
groups
id
```

#### Get group of other user
```
groups username
id username
```

#### Create group
```
groupadd foo
```

#### Check group
```
cat /etc/group
```

#### Get all members of a group
https://www.cyberciti.biz/faq/linux-list-all-members-of-a-group/
```
lid -g groupname
or
cat /etc/group | grep groupname
```

### User management
#### Check user
```
cat /etc/passwd | grep username
```

#### Create user
```
useradd username
```

#### Set passwd for user
```
passwd username
```

https://www.cyberciti.biz/faq/ubuntu-add-user-to-group/
#### Add user to group
```
usermod -a -G groupname username
```
eg:
```
groups test
test : test admins -> test is primary group, admins is secondary group
```

#### Change primary group of user
```
usermod -g groupname username
```
eg:
```
group test
test : admins -> adnins become to primary group
```

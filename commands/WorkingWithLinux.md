```
find . -iname "*retry*" | xargs rm -f
```

Follow: https://askubuntu.com/questions/111495/how-to-diff-multiple-files-across-directories
```
diff -r dir1/ dir2/
```

```
ssh-copy-id -i /path/to/public-key user@host
```

If private key name is different
```
ssh-add ~/.ssh/id_rsa_xxx
git add -A; git commit -m "Add"; git push  -u origin master
git pull
```

```
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa_xxx; git add -A; git commit -m "Add"; git push  -u origin master'
ssh-agent bash -c 'ssh-add ~/.ssh/id_rsa_xxx; git pull'
```

```
ln -s /path/to/origin/dir /path/to/symlink
```

```
groups
```

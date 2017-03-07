# Copy public key
```
ssh-copy-id -i /path/to/public-key user@host
```

# Use key to commit code
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

Up VM
```
vagrant up
```

Shutdown VM
```
vagrant halt
```

Destroy VM
```
vagrant destroy
```

Restart VM
```
vagrant reload
```

Update package in VM
```
vagrant reload --provision
```

SSH to VM
```
vagrant ssh
```

Get global status
```
vagrant global-status
```

Share vagrant via ssh
```
https://ngrok.com/download
https://ngrok.com/signup
https://dashboard.ngrok.com
vagrant share --ssh
vagrant connect --ssh NAME
```

Packaging to a box
```
vagrant package --base <UUID-of-vm> --output NAME
```

View port
```
vagrant port my-machine
```

# Check version
```
https://<domain>/help
gitlab-rake gitlab:env:info
rpm -qa | grep gitlab
```

# Check configure
```
gitlab-rake gitlab:check
```

# Check gitlab status
```
gitlab-ctl status
```

# Restart gitlab
```
gitlab-ctl restart
gitlab-ctl restart nginx|postgresql|redis|sidekiq
gitlab-ctl reconfigure
```

# Backup gitlab
```
gitlab-rake gitlab:backup:create
```

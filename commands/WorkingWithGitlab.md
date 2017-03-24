# Check version
```
https://<domain>/help
```

```
rpm -qa | grep gitlab
```

# Validate .gitlab-ci.yml
```
https://<domain>/ci/lint
```

```
Project Settings > Pipelines
```

# Check runner
```
https://<domain>/<user>/<project>/settings/ci_cd
```

```
Project Settings > CI/CD Pipelines
```

# Check pipelines and jobs
```
https://<domain>/<user>/<project>/pipelines
https://<domain>/<user>/<project>/builds
```

```
Project Settings > Pipelines > Pipelines
Project Settings > Pipelines > Jobs
```

# View log jobs
```
Project Settings > Pipelines > Jobs > Click on job status
```

# Get shared runner token
```
https://<domain>/admin/runners
```

# Check ci runner list
```
sudo gitlab-ci-multi-runner list
```
```
gitlab-runner list
```

# Check ci runner status
```
sudo gitlab-ci-multi-runner status
```

# Restart gitlab
```
gitlab-ctl reconfigure
```

# Unregister runner
```
gitlab-runner unregister --name="runner-name"
```

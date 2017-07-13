## Check ssh
```
ssh -vT git@<git-domain>
less /var/opt/gitlab/.ssh/authorized_keys
```

## Add - Commit - Push
```
git add -A
git commit -m "msg"
git push -u origin master
```

## Clone
```
git clone remote_url
```

## Pull
```
git pull
```

## Check status
```
git status
```

## Config user.name and user.email
```
git config --list
git config user.name "name"
git config user.email "email"
git remote add origin http://IP/path/to/repository.git
or change
git remote set-url origin https://github.com/USERNAME/REPOSITORY.git
If you use ssh then origin is ssh
You must have declare key to push
```

## Diff
```
changed but not staged
git diff <file>
```

## View log
```
git log
git log -p -2
git log --oneline --decorate --graph --all
```

## View remote URL
```
git remote -v
git remote show origin/upstream/<repo-name>
```

## View branches
```
git branch -v
```

## Create new branch and select branch
```
git checkout -b branch_name
git checkout branch_name
```

## Create branch base on other branch
```
git checkout -b other-branch new-branch
```

## Revert local
```
git checkout -- /path/to/file
```

## Delete a local branch
```
git branch -D branch_name ### equal git branch -d --force branch_name
git branch -d branch_name
```

## add - commit - push to branch
```
git add . ## add to staging (index)
git commit -m "msg" ## add to local repo
git push remote_name branch_name ## add to remote repo
```

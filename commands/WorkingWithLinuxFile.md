# Delete file in a path
```
find . -iname "*retry*" | xargs rm -f
```

# Check differences
Follow: https://askubuntu.com/questions/111495/how-to-diff-multiple-files-across-directories
```
diff -r dir1/ dir2/
```

# Create softlink
```
ln -s /path/to/origin/dir /path/to/symlink
```

# Sort file/dir by modification time
```
ls -lt /path/to/dir ### order by asc
ls -ltr /path/to/dir ### order by desc
```

# Remove folder order than a specific day
https://unix.stackexchange.com/questions/92346/why-does-find-mtime-1-only-return-files-older-than-2-days
```
base_output=/data/local-backup
find ${base_output} -type d | xargs rmdir > /dev/null ### remove empty dir, redirect if rm non empty dir
find ${base_output} -mtime +1 | xargs rm -rf ### rm files whose age is order than 2 days -> Keep files whose age less than 2 days
```

# Ensure a contanst number of folder
```
base_output=/data/local-backup
ls -td1 ${base_output}/*/ | tail -n +2 | xargs rm -rf
```

# Encrypt files
https://askubuntu.com/questions/17641/create-encrypted-password-protected-zip-file
```
zip --encrypt file.zip files ### enter pass to zip
unzip file.zip ### enter pass to unzip
```

# Calculate disk space
```
df -Th
```

```
du -h --max-depth=1 --exclude=/var
```

```
ncdu
```

# Keep files for last 15 days
```
ls -lt | tail -n +15
```

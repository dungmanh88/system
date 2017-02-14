https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-php

heroku login
git init
git add .
git config user.name
git config user.email
heroku create php-intro
echo '{}' > composer.json
git add composer.json
git commit -m "add composer.json for PHP app detection"
heroku buildpacks:set heroku/php

heroku logs --tail

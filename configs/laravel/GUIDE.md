# Install composer
https://getcomposer.org/
```
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"

php -r "if (hash_file('SHA384', 'composer-setup.php') === '669656bab3166a7aff8a7506b8cb2d1c292f042046c5a994c43155c0be6190fa0355160742ab2e1c88d40d5be660b410') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"

php composer-setup.php
php -r "unlink('composer-setup.php');"
```
You will get composer.phar
```
mv composer.phar /usr/local/bin/composer
```

# Install mcrypt
https://stackoverflow.com/questions/16830405/laravel-requires-the-mcrypt-php-extension
```
yum install -y php-mcrypt php-mbstring php-xml
```

# Install laravel
https://laravel.com/docs/5.4/installation
```
Do not run Composer as root/super user! See https://getcomposer.org/root for details

If you do not have existing project
```
composer create-project laravel/laravel ImgStore --prefer-dist
```
You get done when you get Application key

If you have a existing project
```
cd ImgStore/
composer install
cp .env.example .env
rm -f .gitignore
php artisan key:generate
php artisan config:clear
php artisan migrate
```

cd ImgStore/
php artisan serve
Laravel development server started: <http://127.0.0.1:8000>

curl -I localhost:8000
HTTP/1.1 200 OK
Install successfully
```

# Manage php artisan
```
php artisan --version
Laravel Framework 5.4.33
```
```
php artisan serve
```
Create migration in database/migrations
```
php artisan make:migration migration_name
```
Create migration for session table
```
php artisan session:table
```
Create table to keep track migrations
```
php artisan migrate:install
```
Migrate from database/migrations into real db - run up function
```
php artisan migrate
```
Rollback migrations - run down function
```
php artisan migrate:rollback
```
Make model
```
php artisan make:model model_name
```
```
composer require laravelcollective/html
```
# Structure
Route
```
routes/web.php
```
Assets
```
public/css
public/js
index.php
```
View
```
resources/views/*.blade.php
```
Database config
```
config/database.php
```
Migration:
```
database/migrations
```

# Some features:
```
SchemaBuilder
Migration
```

# Log
config/app.php
```
    'debug' => env('APP_DEBUG', true),
```
```
storage/logs/laravel.log
```

# Config
```
.env (primary config)
config/database.php (secondary config)
```

# Migrate
make migration -> create schema -> migrate -> make model
-> access db via model

# Add class
https://stackoverflow.com/questions/43207428/laravel-5-4-class-form-not-found
https://stackoverflow.com/questions/31696679/laravel-5-class-input-not-found

# DB Conventions
table name is plural

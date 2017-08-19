```
php artisan make:migration create_paintings
```
In database/migrations/timestamp_create_paintings.php, you implement
up and down function
```
public function up()
{
    //
    Schema::create('paintings', function($thePainting){
      $thePainting->increments('id');
      $thePainting->string('title');
      $thePainting->string('artist');
      $thePainting->integer('year');
      ### timestamps will log create_at and last modified at of record
      $thePainting->timestamps();
    });
}

/**
 * Reverse the migrations.
 *
 * @return void
 */
public function down()
{
    //
    Schema::drop('paintings');
}
```

Make sure that in config/database.php
```
    'migrations' => 'migrations',  ### table to keep track migrations
```
```
php artisan migrate:install
```
```
php artisan migrate
```
```
php artisan migrate:rollback
```
```
php artisan make:model Painting
```
**You should use plural name for table, and singular name for model**
You should get a class in app/Painting.php

Implement this class and use the class in routes

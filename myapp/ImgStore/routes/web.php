<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('about', function () {
    return 'About content goes here';
});

Route::get('about/directions', function () {
    return 'Directions goes here';
});

Route::get('about/{theSubject}', function ($theSubject) {
    return $theSubject . ' goes here';
});

Route::get('about/classes/{theSubject}', function ($theSubject) {
    return "Content about $theSubject classes goes here";
});

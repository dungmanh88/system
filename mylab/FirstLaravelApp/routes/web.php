<?php
use App\Painting;
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
  // Schema::create('art', function($newtable){
  //  $newtable->increments('id');
  //  $newtable->string('artist');
  //  $newtable->string('title', 500);
  //  $newtable->text('description');
  //  $newtable->date('created');
  //  $newtable->date('exhibition_date');
  //  $newtable->timestamps();
  // });
  //
  // Schema::table('art', function($newtable){
  //  $newtable->boolean('alumni');
  //  $newtable->dropColumn('exhibition_date');
  // });
  // $painting = new Painting;
  // $painting->title = "Do no wrong";
  // $painting->artist= "Do it right";
  // $painting->year = 2014;
  // $painting->save();
  // return view('welcome');
  // $painting = Painting::find(1);
  // $painting->title = "Do it right now!!!";
  // $painting->save();
  // return $painting->title;
  $theLandmarks = array('St. Marks', 'Central Park', 'Times square');
  return view('welcome', array('theLocation' => 'NYC', 'theWeather' => 'stormy', 'theLandmarks' => $theLandmarks));
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

Route::get('signup', function(){
  return view('signup');
});

Route::post('thanks', function(){
  $theEmail = Input::get('email');
  return view('thanks')->with('theEmail', $theEmail);
});

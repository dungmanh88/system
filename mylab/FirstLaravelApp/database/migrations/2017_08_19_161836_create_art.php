<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateArt extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        //
        Schema::create('art2', function($newtable){
          $newtable->increments('id');
          $newtable->string('artist');
          $newtable->string('title', 500);
          $newtable->text('description');
          $newtable->date('created');
          $newtable->boolean('alumni');
          $newtable->timestamps();
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
        Schema::drop('art2');
    }
}

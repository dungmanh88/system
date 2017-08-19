Schema::create('art', function($newtable){
 $newtable->increments('id');
 $newtable->string('artist');
 $newtable->string('title', 500);
 $newtable->text('description');
 $newtable->date('created');
 $newtable->date('exhibition_date');
 $newtable->timestamps();
});

Schema::table('art', function($newtable){
 $newtable->boolean('alumni');
 $newtable->dropColumn('exhibition_date');
});

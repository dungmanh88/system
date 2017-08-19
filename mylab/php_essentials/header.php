<?php
  function test(){
    echo "123";
  }
  header("HTTP/1.1 404 NOT FOUND");
 ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html lang="en">
	<head>
		<title>untitled</title>
	</head>
	<body>
    <?php
      //header("HTTP/1.1 404 NOT FOUND");
     ?>
	</body>
</html>

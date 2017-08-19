<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html lang="en">
	<head>
		<title>untitled</title>
	</head>
	<body>
    <?php
    $input = 0.0;
    if (!isset($input) || empty($input)) {
      echo "Validation failed 1 <br />";
    }
    $input = "abcd";
    $min = 3;
    $max = 9;
    if (strlen($input) < $min || strlen($input) > $max){
      echo "Validation failed 2 <br />";
    }


    $input = 1;
    if (!is_string($input)) {
      echo "Validation failed 3 <br />";
    }

    $input = 7;
    $set = array(1,3,5,6);
    if(!in_array($input, $set)) {
      echo "Validation failed 4 <br />";
    }

    $input = "phx is suck";
    if (!preg_match("/PHP/i", $input)) {
      echo "Validation failed 5 <br />";
    }

    $input = "something!somewhere";
    if (strpos($input, "@") === false){
      echo "Validation failed 6 <br />";
    }
    ?>
	</body>
</html>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html lang="en">
	<head>
		<title>First Page</title>
	</head>
	<body>
    <?php
      $link_name = "Second Page";
      $my_name = "This is a string with < > Johnson & BM $#?&";
      $text = '<Click here> "& This is a link"?';
      $url = rawurlencode($link_name) . ".php?";
      $url .= "name=" . urlencode($my_name);
      for($i=1; $i<=10; $i++){
        $id = $i;
     ?>
    <a href="<?php echo htmlentities($url . "&id=$id"); ?>"><?php echo htmlentities($text . $id); ?></a>
    <?php
      }
     ?>
	</body>
</html>

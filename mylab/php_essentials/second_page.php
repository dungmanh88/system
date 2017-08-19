<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html lang="en">
	<head>
		<title>Second Page</title>
	</head>
	<body>
    <?php echo "Welcome you to second page"; ?>
    <pre>
    <?php
      print_r($_GET);
     ?>
   </pre>
   <?php
    $id = $_GET['id'];
    echo "You have request resource with id = $id";
    ?>
	</body>
</html>

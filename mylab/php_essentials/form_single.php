<?php
  if(isset($_POST['submit'])){
    $username = $_POST['username'];
    $password = $_POST['password'];
    $message = "You are logged in, welcome {$username}";
    if ($username == "jack" && $password == "secret"){
      header("Location: basic.html");
    }else{
      $message = "There is something error";
    }
  }else{
    $username = "";
    $message = "Please login, stranger";
  }

 ?>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html lang="en">
	<head>
		<title>Form Single</title>
	</head>
  <?php
    echo "{$message}";
   ?>
	<body>
      <form action="form_single.php" method="POST">
        Username: <input type="text" name="username" value="<?php echo htmlentities($username); ?>" />
        <br />
        Password: <input type="password" name="password" value="" />
        <br />
        <input type="submit" name="submit" value="Submit" />
      </form>
	</body>
</html>

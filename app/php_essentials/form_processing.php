<pre>
<?php
  print_r($_POST);
 ?>
</pre>
<br />
<?php
  if (isset($_POST['submit'])) {
    $username = (isset($_POST['username']) && !empty($_POST['username']) && strlen(trim($_POST['username']))) ? $_POST['username'] : "1";
    $password = (isset($_POST['password']) && !empty($_POST['password']) && strlen(trim($_POST['password']))) ? $_POST['password'] : "1";
  } else{
    $username = "";
    $password = "";
  }
  echo "username = {$username}, password = {$password}";
 ?>

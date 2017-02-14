<?php
  if (isset($_POST["user"]) and $_POST["user"] != ""){
      $user = $_POST["user"];
  }
  if (isset($_POST["password"]) and $_POST["password"] != ""){
      $pass = $_POST["password"];
  }
  if (isset($_POST["ck_rt"]) and $_POST["ck_rt"] == "on"){
      setcookie("user", $user, time() + 3600, "/", "php-intro.herokuapp.com", 0);
      setcookie("pass", $pass, time() + 3600, "/", "php-intro.herokuapp.com", 0);
      setcookie("test", "123", time() + 3600, "/test123", "php-intro.herokuapp.com", 0);
  }
  if (isset($user) and $user != "" and isset($pass) and $pass != ""){
      echo "cam on ban " . $user . " da dang nhap vao he thong voi password la " . $pass;
  }
  elseif (isset($_COOKIE["user"]) and $_COOKIE["user"] != "" and isset($_COOKIE["pass"]) and $_COOKIE["pass"] != "") {
      //header("Location: cookie.php");
      echo "cam on ban " . $_COOKIE["user"] . " da dang nhap vao he thong voi password la " . $_COOKIE["pass"];
      echo "Day la thong tin lay tu cookie";
  }else {
 ?>
<html>
  <form action="cookie.php" method="post">
    Username: <input type="text" name="user" value="" /> <br />
    Password: <input type="password" name="password" value="" /><br />
    <!-- Luu cookie username vao trinh duyet -->
    Remember user: <input type="checkbox" name="ck_rt" /><br />
    <input type="submit" value="Dang Nhap" />
  </form>
</html>
<?php
  }
?>

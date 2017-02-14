<?php
  session_start();
#  $_SESSION["Public"] = "Public Info";
#  $_SESSION["Private"] = "Private Info";
#  echo "session name public = " . $_SESSION["Public"] . "<br />";
  if (isset($_POST["public"]) and $_POST["public"] != "") {
    $_SESSION["public"] = $_POST["public"];
  }
  if (isset($_POST["private"]) and $_POST["private"] != "") {
    $_SESSION["private"] = $_POST["private"];
  }
 ?>
 <html>
<a href="session_test.php">Test</a>
<form action="session.php" method="post">
  Public <input name="public" value="" type="text" /> <br />
  Private <input name="private" value="" type="text" /> <br />
  <input type="submit" value="Submit" />
</form>
</html>

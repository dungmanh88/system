<?php
session_start();
echo "session id is " . session_id(); 
if (isset($_SESSION["public"])) {
  echo "Test: session name public = " . $_SESSION["public"] . "<br />";
}
if (isset($_SESSION["private"])) {
  echo "Test: session name private = " . $_SESSION["private"] . "<br />";
}

//session_destroy();
//$_SESSION = array();
/*
if (isset($_SESSION["public"])) {
  echo "Test: session name public = " . $_SESSION["public"] . "<br />";
}
if (isset($_SESSION["private"])) {
  echo "Test: session name private = " . $_SESSION["private"] . "<br />";
}
*/
 ?>

<?php
  session_start();
  // clean up $_SESSION array or session_destroy()
//  $_SESSION = array();
  unset($_SESSION["public"])
 ?>

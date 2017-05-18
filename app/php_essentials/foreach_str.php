<?php
  $str = "hello";
  $array_str = str_split($str);
  foreach ($array_str as $char) {
    echo $char;
    echo "\n";
  }
  for($i=0; $i<strlen($str); $i++){
    echo $str[$i];
  }
 ?>

<?php
function pre_fizz($n) {
  $fizz_buzz_array = array();
  for($i=1; $i<=$n; $i++){
    array_push($fizz_buzz_array,$i);
  }
  return $fizz_buzz_array;
}


function pre_fizz($n) {
  $arr;
  for($i = 1; $i <= $n; $i++) {
    $arr[] = $i;
  }
  return $arr;
}

?>

<?php
function reverseLetter($str){
  $alphabet_array = array('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z');
  $str_array = str_split($str);
  foreach($str_array as $char){
//    echo $char;
//    echo "\n";
    if(!in_array($char, $alphabet_array)){
        unset($str_array[array_search($char, $str_array)]);
    }
  }
  $reverse_array = array_reverse($str_array);
  return implode($reverse_array);
}

function reverseLetter($str){
  $rev = strrev($str);
  $res = preg_replace("/[\W\d_]/", "", $rev);
  return $res;
}

function reverseLetter(string $str){
  return preg_replace('/[^a-z]/i', '', strrev($str));
}

function reverseLetter($str){
$res = "";

  for ($i = 0; $i < strlen($str); $i++){
    if (ctype_alpha($str[$i])){
      $res .= $str[$i];
    }
  }

return strrev($res);

}

echo reverseLetter("ultr53o?n");
?>

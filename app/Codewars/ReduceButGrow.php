function production($carry, $item){
  $carry *= $item;
  return $carry;
}
function grow($a) {
   return array_reduce($a, "production", 1);
}

function object() {
  if(window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  }
  // ignore old browser like IE5 or IE6
  return xmlhttp;
}

var http = object();
function getbyid(id){
  http.open('get', 'getbyid.php?id=' + id, false);
  http.onreadystatechange = function(){
      if(http.readyState == 4 && http.status == 200) {
        document.getElementById("result").innerHTML = http.responseText;
      }
  }
  http.send();
}

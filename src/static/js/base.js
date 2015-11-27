function which_user(){
 if( document.getElementById("user_one") ==
 document.getElemntById("action_user"))
 {
  document.getElementById("sender").innerHTML =
  document.getElementById("user_two").value
 }
 else if(document.getElementById("user_two") ==
 document.getElementById("action_user"))
 {
  document.getElementById("sender").innerHTML =
  document.getElementById("user_one").value
 }
 }

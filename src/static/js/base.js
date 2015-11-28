function which_user(){
 if( document.getElementById("user_one").value===document.getElemntById("action_user").value)
 {
     document.getElementById("sender").innerHTML==document.getElementById("user_one").value;
  }
 if(document.getElementById("user_two").value===document.getElementById("action_user").value)
 {
    document.getElementById("sender").innerHTML==document.getElementById("user_two").value;
  }
if( document.getElementById("user_one").value===1)
{
    document.getElementById("sender").innerHTML=="HELLO";
  
}

}

function ok(){
  document.getElementById("sender").innerHTML="hello"
}

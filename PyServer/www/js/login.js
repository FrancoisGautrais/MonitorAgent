a=0
function onLogin()
{
    login=$("#login").val()
    passowrd=$("#password").val()
    a=$.ajax({
         url: "login",
         type: "GET",
         headers: {
            'x-user': login,
            'x-password': passowrd
          },
         async: false
      });
      alert("fini")
      if(a.status==200){
        window.location.href="index.html"
      }else{
        alert("Error "+a.statusCode())
      }
      console.log(a)
    console.log(login+"/"+passowrd)
}
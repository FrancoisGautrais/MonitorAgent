a=0
function seterror(str)
{
    $("#error").html(str)
    $("#error-div").show(500)
}

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

    if(a.status==200){
      window.location.href="index.html"
    }else{
      seterror("Mauvais login ou mot de passe")
      console.log("------")
    }
}
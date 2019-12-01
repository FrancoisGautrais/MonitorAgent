
function appendToLog(s)
{
    $("#log").html($("#log").html()+"<br>"+s)
}

function goToByScroll(id) {
    // Remove "link" from the ID
    id = id.replace("link", "");
    // Scroll
    $('html,body').animate({
        scrollTop: $("#" + id).offset().top
    }, 'slow');
}

function scrollDiv(n) {

	if (!ReachedMaxScroll) {
		DivElmnt.scrollTop = PreviousScrollTop;
		PreviousScrollTop++;

		ReachedMaxScroll = DivElmnt.scrollTop >= (DivElmnt.scrollHeight - DivElmnt.offsetHeight);
	}
	else {
		ReachedMaxScroll = (DivElmnt.scrollTop == 0)?false:true;

		DivElmnt.scrollTop = PreviousScrollTop;
		PreviousScrollTop--;
	}
}

function on_send()
{
    cmd=$("#input_command").val()
    $("#input_command").val("")

    appendToLog(cmd)
    $.ajax({
      type: "POST",
      url: "command",
      data: JSON.stringify({
        sync: true,
        cmd: cmd,
        target: $("#id").text()
      }),
      success: on_success,
      error: on_error,
      dataType: "json"
    });
}

function on_error(xhr, err, errorThrown)
{
    M.toast({html: 'Erreur'})
    console.log(err)
    console.log(errorThrown)
}

$('#input_command').keyup(function(e){
    if(e.keyCode == 13)
    {
        on_send()
    }
});

function on_success(data)
{
    M.toast({html: 'Commande envoyée'})
    appendToLog(data.data.stdout)
    var elem = document.getElementById('log');
    elem.scrollTop = elem.scrollHeight;
}
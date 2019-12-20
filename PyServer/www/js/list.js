function on_terminal(id)
{
     M.toast({html: 'reboot'})

}

function on_shutdown(id)
{
     M.toast({html: 'reboot'})
}

function on_reboot(id)
{
     M.toast({html: 'reboot'})
}

function on_options(id)
{
     var $form = $("<form />");

     $form.attr("action", "poste.html");
     $form.attr("method","POST");

     $form.append('<input type="hidden" name="id" value="'+id+'" />');

     $("body").append($form);
     $form.submit();
}


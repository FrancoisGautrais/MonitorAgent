String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};


$(document).ready(function(){
    $('.collapsible').collapsible();
    $("#actiondiv").load("poste_action.html");
    $("#systemdiv").load("poste_system.html");
    $("#procdiv").load("poste_proc.html");

  });

function appendToLog(s)
{

    $("#log").html($("#log").html()+"<br>"+s.replaceAll("\n", "<br>"))
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

function send(cmd, args)
{
    $.ajax({
      type: "POST",
      url: "command",
      data: JSON.stringify({
        sync: true,
        cmd: {
            sync: true,
            cmd: cmd,
            args: args
        },
        target: $("#id").text()
      }),
      success: on_success,
      error: on_error,
      dataType: "json"
    });
}

function send_sync(cmd, args=[])
{
    return $.ajax({
      type: "POST",
      url: "command",
      data: JSON.stringify({
        sync: true,
        cmd: {
            sync: true,
            cmd: cmd,
            args: args
        },
        target: $("#id").text()
      }),
      headers: {
        "Content-Type" : "application/json"
      },
      async: false,
      dataType: "json"
    });
}

function on_send()
{
    cmd=$("#input_command").val()
    $("#input_command").val("")

    appendToLog(cmd)
    $.ajax({
      type: "POST",
      url: "command/texte",
      data: JSON.stringify({
        sync: true,
        cmd: cmd,
        target: $("#id").text()
      }),
      headers: {
        "Content-Type" : "application/json"
      },
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
    if(data.data.code==0) M.toast({html: 'Commande envoyée'})
    else M.toast({html : 'Erreur('+data.data.code+') : '+data.data.stdout})
    if(data && data.data && data.data.cmd && data.data.cmd.cmd=="upload") {
        //appendToLog(getDownloadLink(data.data.stdout))
        window.location.href=getDownloadLink(data.data.stdout)
    }
    else{
        if( !( typeof(data.data.stdout) == "string"))
            data.data.stdout=JSON.stringify(data.data.stdout)
        appendToLog(data.data.stdout)
    }
    var elem = document.getElementById('log');
    elem.scrollTop = elem.scrollHeight;
}

function getDownloadLink(id)
{
    path=window.location.href
    link=path.substring(0,path.search("admin/poste.html"))+"file/"+id
    return link
}

function ff(n, d=2){
    mult=1
    for (var i=0; i<d; i++) mult*=10
    return Math.round(n*mult)/mult
}
mem=0
cpus=0
function cpu_th(id, cpu)
{
    x=$("<tr></tr>")
    x.append($("<td id=\"cpu_th_"+id+"_0\">"+id+"</td>"))
    x.append($("<td  id=\"cpu_th_"+id+"_1\">"+ff(cpu.max/1000, 2)+" MHz </td>"))
    x.append($("<td  id=\"cpu_th_"+id+"_2\">"+ff(cpu.current/1000, 2)+" MHz </td>"))
    x.append($("<td  id=\"cpu_th_"+id+"_3\">"+ff(cpu.percent, 1)+" % </td>"))
    x.append($('<div class="action"><div class="progress"> '+
            ' <div class="determinate" id=\"cpu_th_'+id+'_4\"  style="width: '+ff(cpu.percent, 1)+'%"></div></div>'))
    return x
}

function uppdate_cpu_th(id, cpu)
{
    id="cpu_th_"+id+"_"
    $("#"+id+"1").html(ff(cpu.max/1000, 2)+ " MHz")
    $("#"+id+"2").html(ff(cpu.current/1000, 2)+ " MHz")
    $("#"+id+"3").html(ff(cpu.percent, 1)+ " %")
    $("#"+id+"4").css("width", ff(cpu.max/1000, 2)+ ' %')

}
js=0

function systemtabclick()
{
    if( $("#systemtab").css("display")=="none")
    {
        systemrefresh(true)
    }
}

function systemrefresh(force=false){

    resp=send_sync("monitor")
    js=resp.responseJSON.data.stdout
    mem=js.memory
    cpus=js.cpus
    percent=ff((mem.total-mem.free)/mem.total*100, 2)
    $("#totalmem").html( ff(mem.total/1024/1024/1024, 1) + " Go")
    $("#usedmem").html( ff((mem.total-mem.free)/1024/1024/1024, 1)  + " Go")
    $("#usedmempc").html( ff((mem.total-mem.free)/mem.total*100, 2) + " %")
    $("#memprogress").css("width", ff((mem.active)/mem.total*100, 0)+"%")
    $("#memprogress2").css("left", ff((mem.active)/mem.total*100, 0)+"%")
    $("#memprogress2").css("width", ff(( (mem.total-mem.free)-mem.active)/mem.total*100, 0)+"%")

    if(sys_body.children().length==0)
    {
        sys_body.append(cpu_th("Moyenne", js.cpus.global))
        for (var i=0; i<cpus.count; i++)
            sys_body.append(cpu_th(i, cpus[i]))
    }else{
        uppdate_cpu_th("Moyenne", js.cpus.global)
        for (var i=0; i<cpus.count; i++)
            uppdate_cpu_th(i, cpus[i])
    }
    if( force || $("#systemtab").css("display")!="none")
        setTimeout(systemrefresh, 2000)
}

function proctabclick()
{
    if( $("#proctab").css("display")=="none")
    {
        procrefresh(true)
    }
}

fields=["pid", "name", "cpu_percent", "memory_percent", ]

function formattime(n)
{
    j=ff(n/(3600*24),0)

    h=ff( (n%(3600*24))/(3600),0)

    m=ff( (n%3600)/60, 0)

    s=ff(n%60,3)

    out=""
    if(j>0) out+=j+" j "
    if(h>0 || j>0) out+=h+" h "
    if(m>0 || j>0 || h>0) out+=m+" m "
    return  out+ff(s,0)+" s"
}

function process_th(data)
{
    id=proc.pid
    id="proc_th_"+id+"_"
    x= $("#"+id)
    if( x.length==0)
    {
        x=$("<tr id=\""+id+"\"></tr>")
        x.append($('<td id="0'+id+'">'+data.pid+'</td>'))
        x.append($('<td id="1'+id+'">'+data.name+'</td>'))
        x.append($('<td id="2'+id+'">'+ff(data.cpu_percent,2)+'</td>'))
        x.append($('<td id="3'+id+'">'+ff(data.memory_percent,2)+'</td>'))
        x.append($('<td id="4'+id+'">'+formattime(Date.now()/1000-data.create_time)+'</td>'))
        x.append($('<td id="5'+id+'"></td>'))
        if(!_proc_filter(id, proc.name)){
            x.hide()
        }
        return x
    }
    $("#0"+id).html(data.pid)
    $("#1"+id).html(data.name)
    $("#2"+id).html(ff(data.cpu_percent,2))
    $("#3"+id).html(ff(data.memory_percent,2))
    $("#4"+id).html(formattime(Date.now()/1000-data.create_time))
    return undefined
}

pids=[]
procnames=[]
_filter=""

function _proc_filter(pid, name)
{
    return name.toLowerCase().search(_filter.toLowerCase())>=0 || (""+pid).search(_filter)>=0
}

function proc_filter(f)
{
    _filter=f
    for(var i=0; i<pids.length; i++)
    {
        id="proc_th_"+pids[i]+"_"
        if( _proc_filter(pids[i], procnames[i]) )
        {
            $("#"+id).show()
        }else{
            $("#"+id).hide()
        }
    }
}


function procrefresh(force=false){
    npids=[]
    resp=send_sync("ps", ["small"])
    //proc_body.empty()
    js=resp.responseJSON.data.stdout
    procnames=[]

    for(var i=0; i<js.length; i++)
    {
        proc=js[i]
        x=process_th(proc)
        npids.push(proc.pid)
        procnames.push(proc.name)
        if(x)
        {
            proc_body.append(x)
        }
    }

    for(var i=0; i<pids.length; i++)
    {
        p=pids[i]
        ok=true
        for(var j=0; j<npids.length; j++)
        {
            if( npids[j]==p){
                ok=false
                break
            }
        }
        if (ok){
            id="proc_th_"+p+"_"
            $("#"+id).remove()
        }
    }

    pids=npids
    if( force || $("#proctab").css("display")!="none")
        setTimeout(procrefresh, 5000)

}
const Client = require("./client.js")
const Utils = require("./utils.js")


class Server{

  constructor()
  {
    this._clients={}
    this._allClients={}
    var t=this
    setTimeout(function (){
      t.cleanDisconnected()
    }, Server.CLEAN_INTERVAL*1000)
  }

  connect(info, ip)
  {
    var x=new Client(info, ip)

    for (var k in this._clients){
      if(this._clients[k].mac==x.mac)
        delete this._clients[k]
    }
    this._clients[ip]=x
    this._allClients[x.uuid]=x
    return x.beginRequest()
  }

  acquireClient(ip)
  {
    if (ip in this._clients){
      return this._clients[ip].beginRequest()
    }
    return null
  }

  disconnect(ip)
  {
    this._clients[ip]=null
  }

  static doFor(list, fct)
  {
    for( var i in list){
      fct(list[i])
    }
  }

  clients()
  {
    var out=[]
    for (const ip in this._allClients){
      out.push(this._allClients[ip])
    }
    return out
  }

  foreach(fct){
    Server.doFor(clients, fct)
  }

  findClientById(host){
    var out=[]
    for (const ip in this._clients){
      var obj = this._clients[ip]
      if(obj._info.name==host){
        out.push(obj)
      }
    }
    return out
  }

  connectedCount()
  {
    return Object.keys(this._clients).length
  }

  cleanDisconnected()
  {
    console.log("Before : "+this.connectedCount())
    for (var k in this._clients){
      var client = this._clients[k]
      if(Utils.time(client._lastRequest)>Server.TIME_TO_DISCONNECT){
        delete this._clients[k]
      }
    }
    console.log("After : "+this.connectedCount())
    var t=this
    setTimeout(function (){
      t.cleanDisconnected()
    }, Server.CLEAN_INTERVAL*1000)
  }

}

Server.TIME_TO_DISCONNECT=10
Server.CLEAN_INTERVAL=10
module.exports=Server

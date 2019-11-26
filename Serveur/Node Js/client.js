const SyncMutex = require('./syncmutex.js');
const CommandQueue = require("./commandqueue.js")
const Utils = require("./utils.js")



class Client {
  constructor(js, ip){
    this._info=js
    this._lastRequest=Utils.time()
    this._statusMutex = new SyncMutex();
    this._queue=new CommandQueue()
    this._connected = Client.STATUS_CONNECTED
  }

  beginRequest(){
    var t=this
    this._statusMutex.lock()
    t._lastRequest=Utils.time()
    t._connected = Client.STATUS_CONNECTED
    this._statusMutex.release()
    return this
  }

  endRequest(){
    var t=this
    this._statusMutex.lock()
        t._lastRequest=Utils.time()
        t._connected = Client.STATUS_WAITING
        setTimeout(function(){
          t._statusMutex.lock()
            t._connected = Client.STATUS_DISCONNECTED
          t._statusMutex.release()
        }, 5000)
    this._statusMutex.release()
  }

  getStatus()
  {
    var status=null
    var t=this
    this._statusMutex.lock()
      status=t._connected
    this._statusMutex.release()
    return status
  }



  send(data)
  {
    this._queue.enqueue(data)
  }

  poll()
  {
    return this._queue.dequeue()
  }



}

Client.STATUS_CONNECTED="CONNECTED"
Client.STATUS_WAITING="WAITING"
Client.STATUS_DISCONNECTED="DISCONNECTED"

module.exports=Client

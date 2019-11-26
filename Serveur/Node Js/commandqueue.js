const Command = require("./command.js")
const Mutex = require('./syncmutex.js');
const sleep = require('sleep');

class CommandQueue {

  constructor(){
    this.data=[]
    this.mutex=new Mutex();
  }

  enqueue(data)
  {
    var t=this
    this.mutex.lock()
    t.data.push(data)
    this.mutex.release()
  }
/*
  dequeue()
  {
    var out=null
    while(out==null){
      out=this._dequeue()
      if(out==null) sleep.msleep(10)
    }
    return out
  }*/

  dequeue()
  {
    var out=[]
    this.mutex.lock()
    console.log(this.data)
    out=this.data
    this.data=[]
    this.mutex.release()
    return out
  }

}
module.exports=CommandQueue

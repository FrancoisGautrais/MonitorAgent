const uuid = require("uuid")

class Command {
  constructor(cmd, args){
    this.id=uuid.v4()
    this.cmd=cmd
    this.args=args
  }

  toJsonString()
  {
    console.log(this.__dict__)
    return JSON.stringify(this.__dict__)
  }

  static halt(){ return new Command("halt")}
  static reboot(){ return new Command("reboot")}
  static print(title, msg){ return new Command("print", [title, msg])}
}

module.exports=Command

module.exports={
  time: function (ref=0)
  {
    return new Date().getTime()/1000-ref
  }
}

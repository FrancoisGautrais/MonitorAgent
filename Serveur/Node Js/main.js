var express = require('express');
var Command = require('./command.js');
const bodyParser = require('body-parser');
const Server = require('./server.js');
const { Worker } = require("worker_threads")
const path = require("path")
const uuid = require("uuid")
const Error = require("./errors.js")
var server=new Server()
var app = express();


function checkSessionId(req, res)
{
  x=req.headers["x-session-id"]
  if(!x){
    res.status(Error.BAD_PARAMETER)
    res.end(JSON.stringify({ code: Error.BAD_PARAMETER, message: "No session id given"}));
    return false
  }
  return true
}


function checkClientFound(req, res, client)
{
  if(!client){
    res.status(Error.BAD_SESSION)
    res.end(JSON.stringify({ code: Error.BAD_SESSION, message: "Bad session id ("+req.headers["x-session-id"]+")"}));
    return false
  }
  return true
}

app.use(bodyParser.json());

function getClientIp(req){
  return req.headers['x-forwarded-for'] || req.connection.remoteAddress
}

app.post('/connect', function(req, res) {
    console.log("connect begin "+Object.keys(server._clients).length)
    req.body.ip=getClientIp(req)
    var id=uuid.v4()
    client = server.connect(req.body, id)

    res.setHeader('Content-Type', 'application/json');
    res.setHeader('x-session-id', id);

    res.end("{ \"code\" : 200, \"message\": \"OK\" }");
    client.endRequest(JSON.stringify(req.body))
    console.log("connect end")
    console.log(server._clients)
    server.findClientById("Fanch-Fixe")[0].send(Command.print("salut", "ça va ?"))

});

app.get('/getinfo', function(req, res) {
    console.log("getinfo begin")
    checkSessionId(req, res)
    client = server.acquireClient(req.headers["x-session-id"])
    checkClientFound(req, res, client)
    res.setHeader('Content-Type', 'application/json');

    res.end(JSON.stringify({ code: Error.OK, message: "OK", data: client}));
    client.endRequest()
    console.log("getinfo end")
});


app.get('/poll', function(req, res) {
    console.log("poll begin")
    checkSessionId(req, res)
    client = server.acquireClient(req.headers["x-session-id"])
    checkClientFound(req, res, client)
    res.setHeader('Content-Type', 'application/json');

    res.end(JSON.stringify({ code: Error.OK, message: "OK", data: client.poll()}));
    client.endRequest()


    console.log("poll end")
});

app.get('/close', function(req, res) {
    console.log("disconnect begin")
    checkSessionId(req, res)
    server.disconnect(req.headers["x-session-id"])
    res.end();
    console.log("disconnect end")
});

app.use('/', express.static(path.join(__dirname, 'www')));



app.listen(8080);

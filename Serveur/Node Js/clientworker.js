var sleep = require("sleep")
const { parentPort, data } = require("worker_threads")
const { data, res, req } = data


console.log("Thread begin")
sleep.sleep(10)
console.log("Thread end")
res.setHeader('Content-Type', 'application/json');
res.end(client.waitForCommand());

client.endRequest()

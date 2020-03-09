const http = require('http');
const url = require("url");

const fs = require('fs');

const requestListener = function (req, res) {
    if(req.url !== "/favicon.ico") {
        console.log("\n\n\n******************** NEW CLIENT ********************\n");
        let u = url.parse("http://localhost"+req.url, true);
        console.log(req.url);

        if("stop" in u) {
            server.shutdown(function (error) {
                if(error) {
                    console.log(error);
                } else {
                    console.log("Node server stopped")
                }
            })
        }

        let json = require("./db.json");

        try {
            json[u.query["paymentId"]] = u.query;
            console.log(json);

            let data = JSON.stringify(json);
            fs.writeFileSync('db.json', data);

            res.statusCode=200;
            res.end("Ok");
        }
        catch(e) {
            res.statusCode = 405;
            res.end("Method not allowed. Stack trace : "+e);
        }
    }
};

var server = http.createServer(requestListener);
server = require("httpshutdown")(server);
server.listen(3000);
console.log("Server started");
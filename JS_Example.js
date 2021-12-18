const requests = require('request');
const fs = require('fs');
const HWID = require('node-hwids');

const readline = require("readline");

const hwid = HWID.getHWID();


const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

var daomain = "domain";
var apikey = "API Key here";
var auser = null;
var apass = null;



console.log(FgGreen, "[AUTH] Enter your Username and password");
rl.question(" Username:", function(user) {
    auser = user;
    rl.question(" Password:", function(pass) {
        apass = pass;
        heads = {"user-agent":"Mozilla/5.0"}
        var authurl = "https://" + daomain + "/api.php?user=" + auser + "&pass=" + apass + "&hwid=" + hwid + "&key=" + apikey;
        request({ url: authurl, headers: heads}, function (error, response, body)
        {
            if (error) {
                console.log(FgRed, "[AUTH] Error: " + error);
                process.exit(1);
            }
            else {
                var json_data = JSON.parse(body);
                if(json_data["status"] == "success") {
                    console.log(FgGreen, "[AUTH] Successfully logged in!");
                    rl.close();
                }
                else {
                    console.log(FgRed, "[AUTH] Failed to log in!");
                    console.log(FgRed, "[AUTH] Error: " + json_data["error"]);
                    process.exit(1);
                }
            }
        });
    });
});


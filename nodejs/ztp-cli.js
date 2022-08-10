require('dotenv').config({ path: __dirname + '/.env' });
var axios = require('axios');
var readline = require('readline');
var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});
rl.question("What is the MAC?", function (answer) {
    console.log("You entered ", answer);
    rl.close();
});
var config = {
    headers: {
        "API-KEY": process.env["APIKEY"]
    }
};
var url = "https://api.ztp.poly.com/preview/devices";
axios
    .get(url, config)
    .then(function (res) {
    console.log("statusCode: ".concat(res.status));
    console.log(res.data.results);
})["catch"](function (error) {
    console.error(error);
});
//console.log(process.env["APIKEY"])

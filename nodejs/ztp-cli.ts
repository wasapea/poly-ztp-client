require('dotenv').config({ path: __dirname+'/.env' })
const axios = require('axios')
const readline = require('readline')

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
})

rl.question("What is the MAC?", function(answer) {
  console.log("You entered", answer)
  rl.close()
})

const config = {
  headers: {
    "API-KEY": process.env["APIKEY"]
  }
}

const url = "https://api.ztp.poly.com/preview/devices"

axios
  .get(url, config)
  .then(res => {
    console.log(`statusCode: ${res.status}`);
    console.log(res.data.results);
  })
  .catch(error => {
    console.error(error);
  });

//console.log(process.env["APIKEY"])
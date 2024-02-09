const https = require('https');
const { convertArrayToCSV } = require('convert-array-to-csv');
const fs = require('fs');

let btc,eth,bch,xrp;
var x = [1,2,3,4];

function row(){

req("btc",0);
req("eth",1);
req("bch",2);
req("xrp",3);


function req(ticker,i){

    var price;
    
    var options = {
        family:4,
        host: 'bitso.com',
        port: 443,
        path: `/api/v3/ticker/?book=${ticker}_usd`,
        method: 'GET'
    };
  
    var req = https.request(options, function(res) {
  
        res.setEncoding('utf8');
        res.on('data', function (chunk) {

        x[i] = Number(JSON.parse(chunk).payload.ask);
  
        console.log(x[i]);
  
        });
    });
  
    req.on('error', function(e) {
        console.log('problem with request: ' + e.message);
    });
  
    req.end();

    
    return price;
}
setTimeout(function() {


var dataArrays = [x];
console.log(dataArrays);

const csvFromArrayOfArrays = convertArrayToCSV(dataArrays, {
    separator: ','
  });

  console.log(csvFromArrayOfArrays);

fs.appendFile("criptos.csv",csvFromArrayOfArrays,err => {

});

}, 1000);

}

let periodos= 36;
let min = 1000*60;
for(let n=0;n<periodos;n++){
    setTimeout(row,5*min*n);
}
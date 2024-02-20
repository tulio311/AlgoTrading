const https = require('https');
const { convertArrayToCSV } = require('convert-array-to-csv');
const fs = require('fs');

var x = [1,2,3,4];

row();

function row(){

req("btc",0);
req("eth",1);
req("bch",2);
req("xrp",3);

function req(ticker,i){

    var price;
    
    var options = {
        family: 4,
        host: 'bitso.com',
        port: 443,
        path: `/api/v3/ticker/?book=${ticker}_usd`,
        method: 'GET'
    };
  
    var req = https.request(options, function(res) {

        res.setEncoding('utf8');
        res.on('data', function (chunk) {

        // Extraction of price
        x[i] = Number(JSON.parse(chunk).payload.ask);

  
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

    const header = ['btc','eth','bch','xrp'];

    const csvFromArrayOfArrays = convertArrayToCSV(dataArrays, {
        header,
        separator: ','
    });

    console.log(csvFromArrayOfArrays);

    fs.writeFile("PreciosNow.csv",csvFromArrayOfArrays,err => {

    });

}, 1000);

}
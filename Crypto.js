const https = require('https');
const { convertArrayToCSV } = require('convert-array-to-csv');
const fs = require('fs');
const { exec } = require("child_process");

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



// Requests loop

let periodos= 36;
let min = 1000*60;

let minBetween = 5

setTimeout(endCall,minBetween*min*(periodos-1)+1000*2);

for(let n=0;n<periodos;n++){
    setTimeout(row,minBetween*min*n);
}




// Adding the boundary mark in the csv, then running 
// the python processing script to process this new data

function endCall(){

    let dots1 = [['.','.','.','.']];
    console.log(dots1)
    const dots = convertArrayToCSV(dots1, {
        //header,
        separator: ','
      });
      console.log(dots) 
    fs.appendFile("criptos.csv",dots,err => {
        if (err) {
            console.error(`append error: ${err}`);
            return;
          }
    });

    exec("python process.py",(error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return;
        }
        console.log(`stdout: ${stdout}`);


        exec("python allModels.py",(error, stdout, stderr) => {
            if (error) {
              console.error(`exec error: ${error}`);
              return;
            }
            console.log(`stdout: ${stdout}`);
    
          });


      });
    
}
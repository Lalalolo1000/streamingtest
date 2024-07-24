var express = require('express');
var fs = require('fs');
var app = express();
var bp = require('body-parser');
const { spawn } = require('child_process');

app.use(bp.json())
app.use(bp.urlencoded({ extended: true }))

// respond with "hello world" when a GET request is made to the homepage
app.get('/earth/*', function(req, res) {
    let url = req.originalUrl;
    let re = /earth\/(?<id>[0-9]+)$/;
    let matches = re.exec(url);
    let id = matches.groups.id;

    let cams = JSON.parse(fs.readFileSync(__dirname + '/cams.json'));

    let script = fs.readFileSync(__dirname + '/earthcam.py', 'utf8');
    script = script.replace('#link#', cams['cam' + id]);
    res.send(script);
});

app.get('/cams.json', function(req, res) {
    res.sendFile(__dirname + '/cams.json');
})

app.get('/edit', function(req, res) {
    res.sendFile(__dirname + '/edit.html');
});

app.post('/save', function(req, res) {
    console.log('Got body:', req.body);
    fs.writeFileSync(__dirname + '/cams.json', JSON.stringify(req.body))
    res.sendStatus(200);
});

// Step 2: Add the /restart endpoint
app.get('/restart', function(req, res) {
    const child = spawn('bash', ['/home/pi/earth/restart_all.sh']);
    child.stdout.on('data', (data) => {
        console.log(`stdout: ${data.toString()}`);
    });
    
    child.stderr.on('data', (data) => {
        console.error(`stderr: ${data.toString()}`);
    });
    
    child.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
    res.sendStatus(200);
});

app.listen(8000);

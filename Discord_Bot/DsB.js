const Discord = require('discord.js');
let {PythonShell} = require('python-shell');
const bot = new Discord.Client();


// console log print of bot connection
bot.on('ready', () => {
    console.log(`Logged in as ${bot.user.tag}!`);
  });

// commands
bot.on('message', (message) => {
    if (message.content == "!commands") {
        message.channel.send("!jenga\n!shake");
    } else if (message.content == "!jenga") {
        message.channel.send("How to win jenga", {files: ["https://i.imgur.com/mjiLIXn.mp4"]}); // files can be image or video urls
    } else if (message.content == "!shake") {
        message.channel.send("thicccc", {files: ["https://i.imgur.com/jSGxuiJ.mp4"]});
    } else if (message.content == "!py"){
        PythonShell.run('data_py.py', null, function (err) { // launches python file
            if (err) throw err;
            console.log('Python File Launched!');
          }); 
        message.channel.sendFile("**add image name / file name here**"); // sends local image file
    } 
});

// token read and login
var fs = require('fs');
fs.readFile('E:/Documents/Discord_Bot/Data_Science_Bot/token', 'utf8', function(error, data){ // hard code in the path of token.txt
    bot.login(data)
});




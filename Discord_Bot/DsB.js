const Discord = require('discord.js');
let {PythonShell} = require('python-shell');
const bot = new Discord.Client();


// console log print of bot connection
bot.on('ready', () => {
    console.log(`Logged in as ${bot.user.tag}!`);
    
  });

  function sleep(miliseconds) { // allows for processing
    var currentTime = new Date().getTime();
    while (currentTime + miliseconds >= new Date().getTime()) {}
 }

// commands
bot.on('message', (message) => {
    if (message.content == "!commands") {
        message.channel.send("Command List:\n !tech\n !salary");
    } else if (message.content == "!jenga") {
        message.channel.send("How to win jenga", {files: ["https://i.imgur.com/mjiLIXn.mp4"]}); // files can be image or video urls
    } else if (message.content == "!shake") {
        message.channel.send("thicccc", {files: ["https://i.imgur.com/jSGxuiJ.mp4"]});
    } else if (message.content == "!tech"){
        message.channel.send("Processing... (5 seconds)");
        PythonShell.run('data_py.py', null, function (err) { // launches python file
            if (err) throw err;
            console.log('Python File Launched!'); // lets host know python file was executed
          }); 
          
        sleep(5000);
        message.channel.sendFile("foo.png"); // sends local image file
    } else if (message.content == "!salary") {

    } else if (message.content == "Hi Data Science Bot"){
        message.channel.send("Hello! I am the Data Science Bot. :smile:");
        message.channel.sendFile("154594528493366171.gif");
        message.channel.send("Type '!commands' to see what I can do");
    }
});

// token read and login
var fs = require('fs'); 

fs.readFile('C:/Users/Archie/Documents/Discord_Bot/Data_Science_Bot/token', 'utf8', function(error, data){ // hard code in the path of token file
    bot.login(data)
});




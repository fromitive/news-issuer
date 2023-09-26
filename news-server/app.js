const express = require('express');
const app=express();
const port=8888;
var bodyParser = require('body-parser');
var fs = require('fs');
var filePath='../news.txt'
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
app.post('/news/send-news', (req,res) => {
	console.log('request received!');
	var content=""
	for(let idx=0; idx <req.body.length ; idx++){
		if(req.body[idx].newsLink && req.body[idx].newsTitle) {
			var line = req.body[idx].newsTitle+"||"+req.body[idx].newsLink+'\n';
			content+=line;
		}	
	}
	console.log('write content\n'+content);
	fs.writeFile(filePath,content,function(err){
		if(err) throw err;
		console.log(filePath+'   saved!!');
	});
	res.send('write ok!');
});

app.listen(port,() => {
	console.log(`Example app listening on port ${port}`)

})

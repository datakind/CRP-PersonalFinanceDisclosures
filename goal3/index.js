const express = require('express');
const app = express();
const port = process.env.Port || 8080;

app.use(express.static('public'));


app.listen(port, () =>{
  console.log('app running on port ', port);
})

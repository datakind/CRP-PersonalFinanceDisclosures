const express = require('express');
const app = express();
const port = process.env.PORT  || 8080;
require('dotenv').config()
app.use(express.static('public'));


app.listen(port, () =>{
  console.log('app running on port ', port);
});
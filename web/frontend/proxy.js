const express = require("express");
const createProxyMiddleware = require('http-proxy-middleware');
var cors = require('cors')

const app = express();
const options = {
   target: 'http://localhost:5000/', //original url
   changeOrigin: true,
   ws: true,
   pathRewrite: {},
   router: {
      'http://127.0.0.1:5000': 'http://127.0.0.1:4000'
   },
   onProxyRes: function (proxyRes, req, res) {
       proxyRes.headers['Access-Control-Allow-Origin'] = '*';
       // proxyRes.headers['Content-Type'] = 'application/json';
    }
}

app.use(cors());

const eProxy = createProxyMiddleware(options);

// app.use('/', createProxyMiddleware({ 
//     target: 'http://localhost:5000/', //original url
//     changeOrigin: true, 
//     ws: true,
//     //secure: false,
//     onProxyRes: function (proxyRes, req, res) {
//        proxyRes.headers['Access-Control-Allow-Origin'] = '*';
//     }
// }));
app.use('/', eProxy);
app.listen(4000);
const http = require('http');
const httpProxy = require('http-proxy');

// Create a proxy server
const proxy = httpProxy.createProxyServer({});

// Create an HTTP server
const server = http.createServer((req, res) => {
  const targetUrl = req.url.slice(1); // Remove the leading slash

  if (!targetUrl) {
    res.writeHead(400, { 'Content-Type': 'text/plain' });
    res.end('No target URL specified');
    return;
  }

  proxy.web(req, res, { target: targetUrl }, (err) => {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('Proxy error: ' + err.message);
  });
});

// Start the server
const port = 8080;
server.listen(port, () => {
  console.log(`Proxy server running on http://localhost:${port}`);
});

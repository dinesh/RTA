#!/usr/bin/env node
express = require('express')
util    = require('util')
fs      = require('fs')

server = express.createServer();

setupRoutes = (server) ->
  server.get '/', (req, res) ->
    res.render 'index.html'
  
startServer = (port, path, callback) ->
  
  server.configure ->
    server.use express.bodyParser()
    server.use express.methodOverride()
    
    server.use express.static(path)
    server.use express.errorHandler({ dumpExceptions: true, showStack: true })
    
    server.set 'views', path 
    server.set 'view options', layout: no
    server.register '.html', compile: (str, options) -> (locals) -> str
    
    server.use server.router
    server.enable 'jsonp callback'
    
    setupRoutes(server)
    
  port = port || process.env.PORT || 3000
  server.listen( parseInt(port, 10) )
  server.on 'listening', callback
  console.log("Starting server on port: " + port)
  server

module.exports = 
  'startServer' : startServer
nib = require 'nib'
stylus = require 'stylus'
sysPath = require 'path'

module.exports = class StylusCompiler
  brunchPlugin: yes
  type: 'stylesheet'
  extension: 'styl'
  generators:
    backbone:
      style: '@import "nib"\n'

  constructor: (@config) ->
    null

  compile: (data, path, callback) ->
    stylus(data)
      .set('compress', yes)
      .set('firebug', !!@config.stylus?.firebug)
      .include(sysPath.join @config.rootPath)
      .include(sysPath.dirname path)
      .use(nib())
      .render(callback)

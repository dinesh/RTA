# Example
# 
#   capitalize 'test'
#   # => 'Test'
#
capitalize = (string) ->
  (string[0] or '').toUpperCase() + string[1..]

# Example
# 
#   formatClassName 'twitter_users'
#   # => 'TwitterUsers'
#
formatClassName = (filename) ->
  filename.split('_').map(capitalize).join('')

module.exports = class JavaScriptCompiler
  brunchPlugin: yes
  type: 'javascript'
  extension: 'js'
  generators:
    backbone: do ->
      types = {}
      ['collection', 'model', 'router', 'view'].forEach (type) ->
        parent = formatClassName type
        types[type] = (fileName) ->
          className = formatClassName fileName
          "exports.#{className} = Backbone.#{parent}.extend({\n\n});"
      types

  constructor: (@config) ->
    null

  compile: (data, path, callback) ->
    try
      callback null, data
    catch error
      callback error

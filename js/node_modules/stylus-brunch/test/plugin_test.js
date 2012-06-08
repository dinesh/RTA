describe('Plugin', function() {
  var plugin;

  beforeEach(function() {
    plugin = new Plugin({});
  });

  it('should be an object', function() {
    expect(plugin).to.be.ok();
  });

  it('should has #compile method', function() {
    expect(plugin.compile).to.be.a(Function);
  });

  it('should compile and produce valid result', function(done) {
    var content = 'body\n  font: 12px Helvetica, Arial, sans-serif';
    var expected = 'body{font:12px Helvetica,Arial,sans-serif}\n';

    plugin.compile(content, 'style.styl', function(error, data) {
      expect(error).not.to.be.ok();
      expect(data).to.equal(expected)
      done();
    });
  });
});

(function(/*! Brunch !*/) {
  if (!this.require) {
    var modules = {}, cache = {}, require = function(name, root) {
      var module = cache[name], path = expand(root, name), fn;
      if (module) {
        return module;
      } else if (fn = modules[path] || modules[path = expand(path, './index')]) {
        module = {id: name, exports: {}};
        try {
          cache[name] = module.exports;
          fn(module.exports, function(name) {
            return require(name, dirname(path));
          }, module);
          return cache[name] = module.exports;
        } catch (err) {
          delete cache[name];
          throw err;
        }
      } else {
        throw 'module \'' + name + '\' not found';
      }
    }, expand = function(root, name) {
      var results = [], parts, part;
      if (/^\.\.?(\/|$)/.test(name)) {
        parts = [root, name].join('/').split('/');
      } else {
        parts = name.split('/');
      }
      for (var i = 0, length = parts.length; i < length; i++) {
        part = parts[i];
        if (part == '..') {
          results.pop();
        } else if (part != '.' && part != '') {
          results.push(part);
        }
      }
      return results.join('/');
    }, dirname = function(path) {
      return path.split('/').slice(0, -1).join('/');
    };
    this.require = function(name) {
      return require(name, '');
    };
    this.require.brunch = true;
    this.require.define = function(bundle) {
      for (var key in bundle)
        modules[key] = bundle[key];
    };
  }
}).call(this);(this.require.define({
  "views/home": function(exports, require, module) {
    (function() {
  var ChartView, IndicatorFormView, SidebarView, SymbolListView, indicatorFormViewTempl, sidebarTmpl, symbolTmpl,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  sidebarTmpl = require('views/templates/sidebar');

  symbolTmpl = require('views/templates/symbols');

  indicatorFormViewTempl = require('views/templates/indicator_form');

  ChartView = require('views/chart');

  IndicatorFormView = (function(_super) {

    __extends(IndicatorFormView, _super);

    function IndicatorFormView() {
      this.render = __bind(this.render, this);
      IndicatorFormView.__super__.constructor.apply(this, arguments);
    }

    IndicatorFormView.prototype.tagName = 'li';

    IndicatorFormView.prototype.initialize = function() {
      IndicatorFormView.__super__.initialize.call(this);
      return this.model = this.options.model;
    };

    IndicatorFormView.prototype.render = function() {
      $(this.el).attr('data-id', "ind-" + this.model.id).data('id', this.model.id).html(indicatorFormViewTempl({
        item: this.model
      }));
      return this;
    };

    return IndicatorFormView;

  })(Backbone.View);

  SidebarView = (function(_super) {

    __extends(SidebarView, _super);

    function SidebarView() {
      this._addIndicator = __bind(this._addIndicator, this);
      this.addIndicator = __bind(this.addIndicator, this);
      this.addIndicatorwithDefault = __bind(this.addIndicatorwithDefault, this);
      this.removeIndicator = __bind(this.removeIndicator, this);
      this.render = __bind(this.render, this);
      SidebarView.__super__.constructor.apply(this, arguments);
    }

    SidebarView.prototype.events = {
      'change select': 'addIndicatorwithDefault',
      'click input.edit': 'addIndicator',
      'click button.close': 'removeIndicator'
    };

    SidebarView.prototype.initialize = function() {
      SidebarView.__super__.initialize.call(this);
      return this.collection.bind('reset', this.render).fetch();
    };

    SidebarView.prototype.render = function() {
      $(this.el).html(sidebarTmpl({
        'items': this.collection.models
      }));
      return this;
    };

    SidebarView.prototype.removeIndicator = function(ev) {
      var indicator, target;
      target = $(ev.currentTarget, this.el).closest('li');
      indicator = this.collection.get(target.data('id'));
      if (indicator) {
        $(target).remove();
        indicator.removeFromChart();
      }
      return this;
    };

    SidebarView.prototype.addIndicatorwithDefault = function(ev) {
      var indicator, target;
      target = $(ev.currentTarget, this.el);
      indicator = this.collection.get(target.val());
      if (indicator) this._addIndicator(indicator, {});
      return this;
    };

    SidebarView.prototype.addIndicator = function(ev) {
      var indicator, indicator_options, target, unfilled;
      target = $(ev.currentTarget, this.el);
      indicator = this.collection.get($(target).data('id'));
      indicator_options = _.map(indicator.get('args'), function(opt) {
        var elem, name;
        name = "" + (indicator.get('id')) + "[" + opt + "]";
        elem = $("[name='" + name + "']");
        return [opt, elem];
      });
      unfilled = _.any(indicator_options, function(p) {
        return _.isEmpty(p[1].val());
      });
      if (unfilled) {
        $(target).closest('li').addClass('alert alert-error');
        return false;
      }
      this._addIndicator(indicator, indicator_options);
      return this;
    };

    SidebarView.prototype._addIndicator = function(indicator, inputs) {
      var callback, symbol, that;
      that = this;
      callback = function(params) {
        var list, options;
        options = _.pick(params, that.collection.validKeys());
        indicator.settings = options;
        list = $('#side-inds-list', that.el);
        if ($("li[data-id='ind-" + indicator.id + "']", list).length < 1) {
          return list.append(new IndicatorFormView({
            model: indicator
          }).render().el);
        }
      };
      if ((symbol = app.ui.companyDp.selectedValue()) && app.models.chart) {
        return indicator.addToChart(inputs, callback);
      } else {
        return alert('No Symbol selected.');
      }
    };

    return SidebarView;

  })(Backbone.View);

  SymbolListView = (function(_super) {

    __extends(SymbolListView, _super);

    function SymbolListView() {
      this.selectedValue = __bind(this.selectedValue, this);
      this.render = __bind(this.render, this);
      SymbolListView.__super__.constructor.apply(this, arguments);
    }

    SymbolListView.prototype.tagName = 'select';

    SymbolListView.prototype.initialize = function() {
      SymbolListView.__super__.initialize.call(this);
      this.container = this.options.container;
      return this.collection.bind('reset', this.render).fetch();
    };

    SymbolListView.prototype.render = function() {
      $(this.el).html(symbolTmpl({
        'items': this.collection.models
      }));
      this.container.append(this.el);
      return this;
    };

    SymbolListView.prototype.selectedValue = function() {
      return $(this.el).val();
    };

    return SymbolListView;

  })(Backbone.View);

  exports.HomeView = (function(_super) {

    __extends(HomeView, _super);

    function HomeView() {
      this.openChart = __bind(this.openChart, this);
      this.render = __bind(this.render, this);
      HomeView.__super__.constructor.apply(this, arguments);
    }

    HomeView.prototype.className = 'container';

    HomeView.prototype.events = {
      'change #symbol-list select': 'openChart'
    };

    HomeView.prototype.render = function() {
      $(this.el).html(require('./templates/home'));
      $('#topbar').html(require('./templates/header'));
      this.subviews = [
        new SidebarView({
          'collection': app.Indicators,
          'el': this.$('#sidebar')
        }), app.ui.companyDp = new SymbolListView({
          'collection': app.Symbols,
          'container': this.$('#symbol-list')
        })
      ];
      return this;
    };

    HomeView.prototype.openChart = function(ev) {
      var model;
      model = app.Symbols.get(this.$(ev.currentTarget).val());
      this.currentChart = new ChartView({
        'model': model,
        'el': this.$('#chart').get(0)
      });
      this.subviews.push(this.currentChart.render());
      return this;
    };

    return HomeView;

  })(Backbone.View);

}).call(this);

  }
}));
(this.require.define({
  "api": function(exports, require, module) {
    (function() {
  var API,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  API = (function() {

    function API(options) {
      this.sync = __bind(this.sync, this);
      this.setUrl = __bind(this.setUrl, this);      options || (options = {});
      this.url = options['url'] || 'http://localhost:5000';
    }

    API.prototype.setUrl = function(url) {
      return this.url = url;
    };

    API.prototype.sync = function(method, model, options) {
      options.timeout = 10000;
      options.dataType = "jsonp";
      options.url = [this.url, options['url'] || model.url].join('/');
      return Backbone.sync(method, model, options);
    };

    return API;

  })();

  module.exports = API;

}).call(this);

  }
}));
(this.require.define({
  "helpers": function(exports, require, module) {
    (function() {

  exports.BrunchApplication = (function() {

    function BrunchApplication() {
      var _this = this;
      $(function() {
        _this.initialize(_this);
        return Backbone.history.start();
      });
    }

    BrunchApplication.prototype.initialize = function() {
      return $.datepicker.setDefaults({
        dateFormat: 'yy-mm-dd',
        onSelect: function(dateText) {
          this.onchange();
          return this.onblur();
        }
      });
    };

    return BrunchApplication;

  })();

}).call(this);

  }
}));
(this.require.define({
  "collections/indicators": function(exports, require, module) {
    (function() {
  var Indicator, Indicators,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  Indicator = require('models/indicator');

  Indicators = (function(_super) {

    __extends(Indicators, _super);

    function Indicators() {
      Indicators.__super__.constructor.apply(this, arguments);
    }

    Indicators.prototype.url = 'api/indicators';

    Indicators.prototype.sync = api.sync;

    Indicators.prototype.model = Indicator;

    Indicators.prototype.parse = function(json) {
      return _.map(json.indicators, function(p) {
        return p;
      });
    };

    Indicators.prototype.validKeys = function() {
      return ['timeperiod', 'matype', 'nbdevdn', 'nbdevup', 'matype', 'slowk_matype', 'slowd_matype', 'fastd_matype', 'cutoff', 'fastperiod', 'slowperiod', 'signalperiod', 'numlines'];
    };

    return Indicators;

  })(Backbone.Collection);

  module.exports = Indicators;

}).call(this);

  }
}));
(this.require.define({
  "models/indicator": function(exports, require, module) {
    (function() {
  var Indicator,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  Indicator = (function(_super) {

    __extends(Indicator, _super);

    function Indicator() {
      this.addToChart = __bind(this.addToChart, this);
      this.removeFromChart = __bind(this.removeFromChart, this);
      this.fullname = __bind(this.fullname, this);
      Indicator.__super__.constructor.apply(this, arguments);
    }

    Indicator.prototype.url = 'api/indicator';

    Indicator.prototype.sync = api.sync;

    Indicator.prototype.fullname = function() {
      return "" + this.id + " - " + (this.get('desc'));
    };

    Indicator.prototype.removeFromChart = function() {
      if (this.charts.length > 0) {
        _.each(this.charts, function(series) {
          return series.remove();
        });
        this.charts = [];
      }
      return this;
    };

    Indicator.prototype.addToChart = function(options, callback) {
      var data, range, symbol, _url,
        _this = this;
      this.charts || (this.charts = []);
      this.removeFromChart();
      if ((symbol = app.ui.companyDp.selectedValue()) && app.models.chart) {
        range = app.models.chart.dateRange();
        _url = [api.url, this.collection.url, this.id, symbol, 'series.json'].join('/');
        data = {
          start: range.dataMin,
          end: range.dataMax
        };
        _.each(options, function(e) {
          return data[e[0]] = e[1].val();
        });
        return $.ajax({
          url: _url,
          dataType: 'jsonp',
          data: data,
          success: function(data) {
            var settings, streams;
            streams = data.records;
            settings = data.settings;
            _.each(streams, function(ts) {
              var onseries, params, yaxis;
              yaxis = parseInt(_.isUndefined(ts.position) ? 2 : ts.position);
              if (ts.series && ts.name) {
                _this.charts.push(app.models.chart.addSeries(ts.name, ts.series, {
                  yAxis: yaxis,
                  id: ts.name,
                  'type': ts.type || 'line'
                }));
                console.log("" + ts.name + " added to chart.");
              }
              if (ts.flags) {
                onseries = ts.name || 'OHLV';
                params = {
                  onSeries: onseries,
                  yAxis: yaxis,
                  type: 'flags',
                  width: 25,
                  shape: 'circlepin'
                };
                return _.each(ts.flags, function(list, title) {
                  _this.charts.push(app.models.chart.addSeries(onseries + ("-" + title), _.map(list, function(e) {
                    return {
                      x: e,
                      title: title
                    };
                  }), params));
                  return console.log("" + (onseries + '-' + title) + " added to chart..");
                });
              }
            });
            if (callback) return callback(settings);
          }
        });
      }
    };

    return Indicator;

  })(Backbone.Model);

  module.exports = Indicator;

}).call(this);

  }
}));
(this.require.define({
  "models/Quoteset": function(exports, require, module) {
    (function() {
  var QuoteSet,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  QuoteSet = (function(_super) {

    __extends(QuoteSet, _super);

    function QuoteSet() {
      QuoteSet.__super__.constructor.apply(this, arguments);
    }

    return QuoteSet;

  })(Backbone.Model);

  module.exports = QuoteSet;

}).call(this);

  }
}));
(this.require.define({
  "routers/main_router": function(exports, require, module) {
    (function() {
  var __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  exports.MainRouter = (function(_super) {

    __extends(MainRouter, _super);

    function MainRouter() {
      MainRouter.__super__.constructor.apply(this, arguments);
    }

    MainRouter.prototype.routes = {
      '': 'home'
    };

    MainRouter.prototype.home = function() {
      return $('body #main').html((app.ui.homeview = app.homeView.render()).el);
    };

    return MainRouter;

  })(Backbone.Router);

}).call(this);

  }
}));
(this.require.define({
  "views/chart": function(exports, require, module) {
    (function() {
  var ChartView, HEIGHTS, MARGIN, OV_HEIGHT, PS_HEIGHT, StockChart,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  HEIGHTS = {
    'overlay': 500,
    'top': 100,
    'bottom': 100,
    'margin': 10
  };

  OV_HEIGHT = HEIGHTS['overlay'];

  PS_HEIGHT = HEIGHTS['top'];

  MARGIN = HEIGHTS['margin'];

  StockChart = (function() {

    function StockChart(el, title, options) {
      var self;
      this.el = el;
      this.title = title;
      this.onChangeDate = __bind(this.onChangeDate, this);
      this.rangeSelector = __bind(this.rangeSelector, this);
      this.dateRange = __bind(this.dateRange, this);
      this.addSeries = __bind(this.addSeries, this);
      $(this.el).css({
        'min-height': '685px'
      });
      this.options = options || {};
      this.items = {
        'overlay': [],
        'top': [],
        'bottom': []
      };
      self = this;
      app.chart = this.handle = new Highcharts.StockChart({
        chart: {
          alignTicks: false,
          renderTo: this.el
        },
        title: {
          text: this.title
        },
        rangeSelector: this.rangeSelector(),
        navigator: {
          enabled: true
        },
        series: options.series || [],
        xAxis: {
          type: 'date',
          zoomType: 'x'
        },
        yAxis: [
          {
            title: {
              text: 'OHLC'
            },
            height: 300
          }, {
            title: {
              text: 'Volume'
            },
            height: 75,
            top: 365,
            offset: 0
          }, {
            title: {
              text: 'Indicator'
            },
            height: 150,
            top: 440,
            opposite: true
          }
        ]
      }, function(_chart) {
        return setTimeout(function() {
          return $('input.highcharts-range-selector', $(_chart.options.chart.renderTo)).datepicker({
            format: 'dd-mm-yyyy'
          }).on('changeDate', self.onChangeDate);
        }, 0);
      });
    }

    StockChart.prototype.addSeries = function(name, series, options) {
      var position, s;
      position = options['position'] || 'overlay';
      this.items[position].push(name);
      s = this.handle.addSeries(_.extend({
        name: name,
        data: series
      }, options));
      if (options['redraw']) this.handle.redraw();
      return s;
    };

    StockChart.prototype.dateRange = function() {
      return this.handle.xAxis[0].getExtremes();
    };

    StockChart.prototype.rangeSelector = function() {
      var sel;
      return sel = {
        selected: 1,
        inputDateFormat: '%d-%m-%Y',
        inputEditDateFormat: '%d-%m-%Y'
      };
    };

    StockChart.prototype.onChangeDate = function(ev) {
      var ed, endDate, instance, option, sd, selectedDate, startDate, _ref;
      selectedDate = ev.date;
      option = (_ref = this.name === "min") != null ? _ref : {
        "minDate": "maxDate"
      };
      instance = $(this).data("datepicker");
      startDate = $("input[name='min']")[0].value;
      endDate = $("input[name='max']")[0].value;
      if (startDate !== "" && endDate !== "") {
        startDate = startDate.split("-");
        endDate = endDate.split("-");
        sd = new Date(Date.UTC(startDate[2], startDate[1] - 1, startDate[0]));
        ed = new Date(Date.UTC(endDate[2], endDate[1] - 1, endDate[0]));
        return this.handle.xAxis[0].setExtremes(sd, ed);
      }
    };

    return StockChart;

  })();

  ChartView = (function(_super) {

    __extends(ChartView, _super);

    function ChartView() {
      this.render = __bind(this.render, this);
      ChartView.__super__.constructor.apply(this, arguments);
    }

    ChartView.prototype.className = 'chart';

    ChartView.prototype.render = function() {
      var url,
        _this = this;
      url = [api.url, 'api/quotes', this.model.get('id') + '.json?'].join('/');
      $.getJSON(url + '&callback=?', function(data) {
        _this.stockchart = new StockChart(_this.el, _this.model.get('id'), {
          series: [
            {
              name: 'OHLV',
              id: 'OHLV',
              data: data.records,
              type: 'candlestick'
            }, {
              name: 'Volume',
              data: data.volume,
              type: 'column',
              yAxis: 1
            }, {
              name: 'Trendline',
              data: data.trendline,
              type: 'line'
            }
          ]
        });
        return app.models.chart = _this.stockchart;
      });
      return this;
    };

    return ChartView;

  })(Backbone.View);

  module.exports = ChartView;

}).call(this);

  }
}));
(this.require.define({
  "application": function(exports, require, module) {
    (function() {
  var API, BrunchApplication, HomeView, Indicator, Indicators, MainRouter, Symbol, Symbols,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  API = require('api');

  window.api = new API();

  BrunchApplication = require('helpers').BrunchApplication;

  MainRouter = require('routers/main_router').MainRouter;

  HomeView = require('views/home').HomeView;

  Indicator = require('models/indicator');

  Indicators = require('collections/indicators');

  Symbol = (function(_super) {

    __extends(Symbol, _super);

    function Symbol() {
      Symbol.__super__.constructor.apply(this, arguments);
    }

    return Symbol;

  })(Backbone.Model);

  Symbols = (function(_super) {

    __extends(Symbols, _super);

    function Symbols() {
      Symbols.__super__.constructor.apply(this, arguments);
    }

    Symbols.prototype.url = 'api/symbols.json';

    Symbols.prototype.sync = api.sync;

    Symbols.prototype.model = Symbol;

    Symbols.prototype.parse = function(json) {
      return _.map(json.records, function(p) {
        return {
          'name': p,
          'id': p
        };
      });
    };

    return Symbols;

  })(Backbone.Collection);

  exports.Application = (function(_super) {

    __extends(Application, _super);

    function Application() {
      Application.__super__.constructor.apply(this, arguments);
    }

    Application.prototype.initialize = function() {
      this.router = new MainRouter;
      this.homeView = new HomeView;
      this.Indicators = new Indicators({
        model: Indicator
      });
      this.Indicator = Indicator;
      this.Symbol = Symbol;
      this.Symbols = new Symbols;
      return this.ui = this.models = {};
    };

    return Application;

  })(BrunchApplication);

  window.app = new exports.Application;

}).call(this);

  }
}));
(this.require.define({
  "views/spinner": function(exports, require, module) {
    (function() {

  app.ui.spinner = {
    show: function(message) {
      this.ensureElement();
      message = message || "Loading";
      return this.el.stop(true, true).fadeIn('fast');
    },
    hide: function() {
      this.ensureElement();
      return this.el.stop(true, true).fadeOut('fast', function() {
        return $(this).css({
          display: 'none'
        });
      });
    },
    ensureElement: function() {
      return this.el || (this.el = $('#spinner'));
    }
  };

  _.bindAll(app.ui.spinner, 'show', 'hide');

}).call(this);

  }
}));
(this.require.define({
  "views/templates/header": function(exports, require, module) {
    module.exports = function (__obj) {
  if (!__obj) __obj = {};
  var __out = [], __capture = function(callback) {
    var out = __out, result;
    __out = [];
    callback.call(this);
    result = __out.join('');
    __out = out;
    return __safe(result);
  }, __sanitize = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else if (typeof value !== 'undefined' && value != null) {
      return __escape(value);
    } else {
      return '';
    }
  }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
  __safe = __obj.safe = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else {
      if (!(typeof value !== 'undefined' && value != null)) value = '';
      var result = new String(value);
      result.ecoSafe = true;
      return result;
    }
  };
  if (!__escape) {
    __escape = __obj.escape = function(value) {
      return ('' + value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };
  }
  (function() {
    (function() {
    
      __out.push('\n<div class=\'navbar navbar-fixed-top\'>\n  <div class=\'navbar-inner\'>\n    <div class=\'container\'>\n      <div class=\'nav-collapse\'>\n        <ul class=\'nav\'>\n          <li class=\'active\'> <a href=\'/\'> DashBoard </a> </li>\n          <li> <a href=\'/\'> Compare </a> </li>\n        </ul>\n      </div>\n    </div>\n  </div>\n</div>\n    ');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
}
  }
}));
(this.require.define({
  "views/templates/home": function(exports, require, module) {
    module.exports = function (__obj) {
  if (!__obj) __obj = {};
  var __out = [], __capture = function(callback) {
    var out = __out, result;
    __out = [];
    callback.call(this);
    result = __out.join('');
    __out = out;
    return __safe(result);
  }, __sanitize = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else if (typeof value !== 'undefined' && value != null) {
      return __escape(value);
    } else {
      return '';
    }
  }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
  __safe = __obj.safe = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else {
      if (!(typeof value !== 'undefined' && value != null)) value = '';
      var result = new String(value);
      result.ecoSafe = true;
      return result;
    }
  };
  if (!__escape) {
    __escape = __obj.escape = function(value) {
      return ('' + value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };
  }
  (function() {
    (function() {
    
      __out.push('\n<div id=\'sidebar\' class=\'span\'>\n</div>\n\n<div id="panel" class="span">\n  <div class=\'page-title\'>\n    <div class=\'pull-right\' id=\'symbol-list\'>\n      \n    </div>\n    \n    <h2> Select the symbol </h2>\n  </div>\n  \n  <div id=\'chart\'> </div>\n</div>');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
}
  }
}));
(this.require.define({
  "views/templates/indicator_form": function(exports, require, module) {
    module.exports = function (__obj) {
  if (!__obj) __obj = {};
  var __out = [], __capture = function(callback) {
    var out = __out, result;
    __out = [];
    callback.call(this);
    result = __out.join('');
    __out = out;
    return __safe(result);
  }, __sanitize = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else if (typeof value !== 'undefined' && value != null) {
      return __escape(value);
    } else {
      return '';
    }
  }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
  __safe = __obj.safe = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else {
      if (!(typeof value !== 'undefined' && value != null)) value = '';
      var result = new String(value);
      result.ecoSafe = true;
      return result;
    }
  };
  if (!__escape) {
    __escape = __obj.escape = function(value) {
      return ('' + value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };
  }
  (function() {
    (function() {
      var item, ma, matypes, option, _i, _j, _len, _len2, _ref;
    
      __out.push('\n');
    
      item = this.item;
    
      __out.push('\n\n<h4>\n  <button class=\'close\'> x </button>\n  <a href="indicator/sidebar/');
    
      __out.push(__sanitize(item.id));
    
      __out.push('"> ');
    
      __out.push(__sanitize(item.fullname()));
    
      __out.push(' </a>\n</h4>\n\n');
    
      if (item.get('args').length) {
        __out.push('\n  <form class=\'form-inline\'>\n    ');
        _ref = item.get('args');
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          option = _ref[_i];
          __out.push('\n      ');
          if (option === 'matype' || option === 'slowk_matype' || option === 'slowd_matype' || option === 'fastd_matype') {
            __out.push('\n        <select name="');
            __out.push(__sanitize(item.get('id')));
            __out.push('[');
            __out.push(__sanitize(option));
            __out.push(']" class=\'input-small\'>\n        ');
            matypes = ['MA_SMA', 'MA_EMA', 'MA_WMA', 'MA_DEMA', 'MA_TEMA', 'MA_TRIMA', 'MA_KAMA', 'MA_MAMA', 'MA_T3'];
            __out.push('\n        ');
            for (_j = 0, _len2 = matypes.length; _j < _len2; _j++) {
              ma = matypes[_j];
              __out.push('\n          <option value="');
              __out.push(__sanitize(_.indexOf(matypes, ma)));
              __out.push('"> ');
              __out.push(__sanitize(ma));
              __out.push(' </option>\n        ');
            }
            __out.push('\n        </select>\n      ');
          } else {
            __out.push('\n            <input class=\'input-small\' placeholder=\'');
            __out.push(__sanitize(option));
            __out.push('\' type=\'text\' \n              name="');
            __out.push(__sanitize(item.get('id')));
            __out.push('[');
            __out.push(__sanitize(option));
            __out.push(']" value="');
            __out.push(__sanitize(item.settings[option]));
            __out.push('"/> \n      ');
          }
          __out.push('\n    ');
        }
        __out.push('\n  </form>\n  \n  <input type=\'button\' data-id="');
        __out.push(__sanitize(item.get('id')));
        __out.push('" class=\'edit btn btn-info\' value=\'Change\' />\n\n');
      }
    
      __out.push('\n');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
}
  }
}));
(this.require.define({
  "views/templates/sidebar": function(exports, require, module) {
    module.exports = function (__obj) {
  if (!__obj) __obj = {};
  var __out = [], __capture = function(callback) {
    var out = __out, result;
    __out = [];
    callback.call(this);
    result = __out.join('');
    __out = out;
    return __safe(result);
  }, __sanitize = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else if (typeof value !== 'undefined' && value != null) {
      return __escape(value);
    } else {
      return '';
    }
  }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
  __safe = __obj.safe = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else {
      if (!(typeof value !== 'undefined' && value != null)) value = '';
      var result = new String(value);
      result.ecoSafe = true;
      return result;
    }
  };
  if (!__escape) {
    __escape = __obj.escape = function(value) {
      return ('' + value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };
  }
  (function() {
    (function() {
    
      __out.push('\n');
    
      __out.push(__sanitize(this.safe(require('views/templates/selects/indicators')({
        items: this.items
      }))));
    
      __out.push('\n<ul id=\'side-inds-list\' class=\'list\'> </ul>');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
}
  }
}));
(this.require.define({
  "views/templates/symbols": function(exports, require, module) {
    module.exports = function (__obj) {
  if (!__obj) __obj = {};
  var __out = [], __capture = function(callback) {
    var out = __out, result;
    __out = [];
    callback.call(this);
    result = __out.join('');
    __out = out;
    return __safe(result);
  }, __sanitize = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else if (typeof value !== 'undefined' && value != null) {
      return __escape(value);
    } else {
      return '';
    }
  }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
  __safe = __obj.safe = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else {
      if (!(typeof value !== 'undefined' && value != null)) value = '';
      var result = new String(value);
      result.ecoSafe = true;
      return result;
    }
  };
  if (!__escape) {
    __escape = __obj.escape = function(value) {
      return ('' + value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };
  }
  (function() {
    (function() {
      var item, _i, _len, _ref;
    
      __out.push('\n<select>\n  ');
    
      _ref = this.items;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        item = _ref[_i];
        __out.push('\n    <option value="');
        __out.push(__sanitize(item.get('id')));
        __out.push('"> ');
        __out.push(__sanitize(item.get('name')));
        __out.push(' </option>\n  ');
      }
    
      __out.push('\n</select>\n  ');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
}
  }
}));
(this.require.define({
  "views/templates/selects/indicators": function(exports, require, module) {
    module.exports = function (__obj) {
  if (!__obj) __obj = {};
  var __out = [], __capture = function(callback) {
    var out = __out, result;
    __out = [];
    callback.call(this);
    result = __out.join('');
    __out = out;
    return __safe(result);
  }, __sanitize = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else if (typeof value !== 'undefined' && value != null) {
      return __escape(value);
    } else {
      return '';
    }
  }, __safe, __objSafe = __obj.safe, __escape = __obj.escape;
  __safe = __obj.safe = function(value) {
    if (value && value.ecoSafe) {
      return value;
    } else {
      if (!(typeof value !== 'undefined' && value != null)) value = '';
      var result = new String(value);
      result.ecoSafe = true;
      return result;
    }
  };
  if (!__escape) {
    __escape = __obj.escape = function(value) {
      return ('' + value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    };
  }
  (function() {
    (function() {
      var item, _i, _len, _ref;
    
      __out.push('\n\n<select>\n  ');
    
      _ref = this.items;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        item = _ref[_i];
        __out.push('\n    <option value="');
        __out.push(__sanitize(item.get('id')));
        __out.push('"> ');
        __out.push(__sanitize(item.get('id')));
        __out.push(' - ');
        __out.push(__sanitize(item.get('desc')));
        __out.push(' </option>\n  ');
      }
    
      __out.push('\n</select>\n');
    
    }).call(this);
    
  }).call(__obj);
  __obj.safe = __objSafe, __obj.escape = __escape;
  return __out.join('');
}
  }
}));

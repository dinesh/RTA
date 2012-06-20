from django import http


class HttpChartResponse(http.HttpResponse):
    '''An HTTP response that returns the chart json config as it's body.''' 
    def __init__(self, chart, content_type=None, **kwargs):
        content_type = content_type or 'application/json'
        super(HttpChartResponse, self).__init__(content=str(chart), content_type=content_type, **kwargs)

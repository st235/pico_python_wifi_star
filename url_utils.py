import json


CONTENT_TYPE_HTML = 'text/html'
CONTENT_TYPE_JSON = 'application/json'

HTTP_CODE_200_OK = '200 OK'
HTTP_CODE_400_BAD_REQUEST = '400 Bad Request'
HTTP_CODE_404_NOT_FOUND = '404 Not Found'
HTTP_CODE_500_INTERNAL_SERVER_ERROR = '500 Internal Server Error'

class HttpRequest:
    def __init__(self,
                 method,
                 url,
                 queries):
        self.__method = method
        self.__url = url
        self.__queries = queries

    @property
    def method(self):
        return self.__method

    @property
    def url(self):
        return self.__url

    @property
    def queries(self):
        return self.__queries
    
    @property
    def has_queries(self):
        return len(self.__queries) > 0
    
    def has_query(self, key):
        return key in self.__queries
    
    def get_query(self, key):
        if key not in self.__queries:
            return None
        return self.__queries[key]
    
    @staticmethod
    def from_raw_request(request):
        raw_request = request.split('\r\n')

        raw_base = raw_request[0].split(' ')
        raw_url = raw_base[1].split('?')

        method = raw_base[0].replace("b'", "")
        url = raw_url[0]
        queries = {}

        if len(raw_url) == 2:
            queries = { rq[0]:rq[1] for rq in [rq.split('=') for rq in raw_url[1].split('&')] if len(rq) == 2}
        
        print('method', method, 'url', url, 'queries', queries)
        return HttpRequest(method, url, queries)
    
    @staticmethod
    def get_http_header(http_code = HTTP_CODE_200_OK,
                        content_type = CONTENT_TYPE_JSON):
        return f'HTTP/1.0 {http_code}\r\nContent-type: {content_type}\r\n\r\n'
    
    @staticmethod
    def get_http_json_reply(obj, http_code = HTTP_CODE_200_OK):
        return str.encode(f'{HttpRequest.get_http_header(http_code, content_type=CONTENT_TYPE_JSON)}{json.dumps(obj)}')

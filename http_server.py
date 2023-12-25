import uasyncio as asyncio
import json

from url_utils import HttpRequest, HTTP_CODE_200_OK, HTTP_CODE_404_NOT_FOUND, CONTENT_TYPE_JSON, CONTENT_TYPE_HTML

METHOD_GET = 'GET'
METHOD_POST = 'POST'

_MIME_TYPES = {
    '.js'     : 'text/javascript',
    '.mjs'    : 'text/javascript',
    '.json'   : 'application/json',
    '.webmanifest': 'application/manifest+json',
    '.doc'    : 'application/msword',
    '.dot'    : 'application/msword',
    '.wiz'    : 'application/msword',
    '.nq'     : 'application/n-quads',
    '.nt'     : 'application/n-triples',
    '.bin'    : 'application/octet-stream',
    '.a'      : 'application/octet-stream',
    '.dll'    : 'application/octet-stream',
    '.exe'    : 'application/octet-stream',
    '.o'      : 'application/octet-stream',
    '.obj'    : 'application/octet-stream',
    '.so'     : 'application/octet-stream',
    '.oda'    : 'application/oda',
    '.pdf'    : 'application/pdf',
    '.p7c'    : 'application/pkcs7-mime',
    '.ps'     : 'application/postscript',
    '.ai'     : 'application/postscript',
    '.eps'    : 'application/postscript',
    '.trig'   : 'application/trig',
    '.m3u'    : 'application/vnd.apple.mpegurl',
    '.m3u8'   : 'application/vnd.apple.mpegurl',
    '.xls'    : 'application/vnd.ms-excel',
    '.xlb'    : 'application/vnd.ms-excel',
    '.ppt'    : 'application/vnd.ms-powerpoint',
    '.pot'    : 'application/vnd.ms-powerpoint',
    '.ppa'    : 'application/vnd.ms-powerpoint',
    '.pps'    : 'application/vnd.ms-powerpoint',
    '.pwz'    : 'application/vnd.ms-powerpoint',
    '.wasm'   : 'application/wasm',
    '.bcpio'  : 'application/x-bcpio',
    '.cpio'   : 'application/x-cpio',
    '.csh'    : 'application/x-csh',
    '.dvi'    : 'application/x-dvi',
    '.gtar'   : 'application/x-gtar',
    '.hdf'    : 'application/x-hdf',
    '.h5'     : 'application/x-hdf5',
    '.latex'  : 'application/x-latex',
    '.mif'    : 'application/x-mif',
    '.cdf'    : 'application/x-netcdf',
    '.nc'     : 'application/x-netcdf',
    '.p12'    : 'application/x-pkcs12',
    '.pfx'    : 'application/x-pkcs12',
    '.ram'    : 'application/x-pn-realaudio',
    '.pyc'    : 'application/x-python-code',
    '.pyo'    : 'application/x-python-code',
    '.sh'     : 'application/x-sh',
    '.shar'   : 'application/x-shar',
    '.swf'    : 'application/x-shockwave-flash',
    '.sv4cpio': 'application/x-sv4cpio',
    '.sv4crc' : 'application/x-sv4crc',
    '.tar'    : 'application/x-tar',
    '.tcl'    : 'application/x-tcl',
    '.tex'    : 'application/x-tex',
    '.texi'   : 'application/x-texinfo',
    '.texinfo': 'application/x-texinfo',
    '.roff'   : 'application/x-troff',
    '.t'      : 'application/x-troff',
    '.tr'     : 'application/x-troff',
    '.man'    : 'application/x-troff-man',
    '.me'     : 'application/x-troff-me',
    '.ms'     : 'application/x-troff-ms',
    '.ustar'  : 'application/x-ustar',
    '.src'    : 'application/x-wais-source',
    '.xsl'    : 'application/xml',
    '.rdf'    : 'application/xml',
    '.wsdl'   : 'application/xml',
    '.xpdl'   : 'application/xml',
    '.zip'    : 'application/zip',
    '.3gp'    : 'audio/3gpp',
    '.3gpp'   : 'audio/3gpp',
    '.3g2'    : 'audio/3gpp2',
    '.3gpp2'  : 'audio/3gpp2',
    '.aac'    : 'audio/aac',
    '.adts'   : 'audio/aac',
    '.loas'   : 'audio/aac',
    '.ass'    : 'audio/aac',
    '.au'     : 'audio/basic',
    '.snd'    : 'audio/basic',
    '.mp3'    : 'audio/mpeg',
    '.mp2'    : 'audio/mpeg',
    '.opus'   : 'audio/opus',
    '.aif'    : 'audio/x-aiff',
    '.aifc'   : 'audio/x-aiff',
    '.aiff'   : 'audio/x-aiff',
    '.ra'     : 'audio/x-pn-realaudio',
    '.wav'    : 'audio/x-wav',
    '.avif'   : 'image/avif',
    '.bmp'    : 'image/bmp',
    '.gif'    : 'image/gif',
    '.ief'    : 'image/ief',
    '.jpg'    : 'image/jpeg',
    '.jpe'    : 'image/jpeg',
    '.jpeg'   : 'image/jpeg',
    '.heic'   : 'image/heic',
    '.heif'   : 'image/heif',
    '.png'    : 'image/png',
    '.svg'    : 'image/svg+xml',
    '.tiff'   : 'image/tiff',
    '.tif'    : 'image/tiff',
    '.ico'    : 'image/vnd.microsoft.icon',
    '.ras'    : 'image/x-cmu-raster',
    '.pnm'    : 'image/x-portable-anymap',
    '.pbm'    : 'image/x-portable-bitmap',
    '.pgm'    : 'image/x-portable-graymap',
    '.ppm'    : 'image/x-portable-pixmap',
    '.rgb'    : 'image/x-rgb',
    '.xbm'    : 'image/x-xbitmap',
    '.xpm'    : 'image/x-xpixmap',
    '.xwd'    : 'image/x-xwindowdump',
    '.eml'    : 'message/rfc822',
    '.mht'    : 'message/rfc822',
    '.mhtml'  : 'message/rfc822',
    '.nws'    : 'message/rfc822',
    '.css'    : 'text/css',
    '.csv'    : 'text/csv',
    '.html'   : 'text/html',
    '.htm'    : 'text/html',
    '.n3'     : 'text/n3',
    '.txt'    : 'text/plain',
    '.bat'    : 'text/plain',
    '.c'      : 'text/plain',
    '.h'      : 'text/plain',
    '.ksh'    : 'text/plain',
    '.pl'     : 'text/plain',
    '.srt'    : 'text/plain',
    '.rtx'    : 'text/richtext',
    '.tsv'    : 'text/tab-separated-values',
    '.vtt'    : 'text/vtt',
    '.py'     : 'text/x-python',
    '.etx'    : 'text/x-setext',
    '.sgm'    : 'text/x-sgml',
    '.sgml'   : 'text/x-sgml',
    '.vcf'    : 'text/x-vcard',
    '.xml'    : 'text/xml',
    '.mp4'    : 'video/mp4',
    '.mpeg'   : 'video/mpeg',
    '.m1v'    : 'video/mpeg',
    '.mpa'    : 'video/mpeg',
    '.mpe'    : 'video/mpeg',
    '.mpg'    : 'video/mpeg',
    '.mov'    : 'video/quicktime',
    '.qt'     : 'video/quicktime',
    '.webm'   : 'video/webm',
    '.avi'    : 'video/x-msvideo',
    '.movie'  : 'video/x-sgi-movie',
}

class HttpServer:
    def __init__(self, 
                 port = 80):
        self.__port = port

        self.__routes = {}
        self.__methods = {}
        self.__content_types = {}

    def on(self, route, handler, 
           method = METHOD_GET,
           content_type = CONTENT_TYPE_JSON):
        assert route not in self.__routes
        self.__routes[route] = handler
        self.__methods[route] = method
        self.__content_types[route] = content_type

    def serve_static(self, file_path):
        file_extension = file_path.split('.')[-1]
        mime_type = _MIME_TYPES[f'.{file_extension}']

        route = f'/{file_path}'
        assert route not in self.__routes

        self.__routes[route] = lambda _: self.__serve_static(file_path)
        self.__methods[route] = METHOD_GET
        self.__content_types[route] = mime_type

    def __serve_static(self, file_path):
        with open(file_path, 'r') as f:
            b = f.read(2048)
            return HTTP_CODE_200_OK, b

    async def __handle_async(self, reader, writer):
        print("Client connected")
        raw_request = await reader.readline()
        raw_request = str(raw_request)
        print("Raw request:", raw_request)

        # We are not interested in HTTP request headers, skip them.
        while await reader.readline() != b"\r\n":
            continue

        http_request = HttpRequest.from_raw_request(raw_request)

        url = http_request.url

        if url not in self.__routes or http_request.method != self.__methods[url]:
            state = {}
            state['error_code'] = 1
            state['error_message'] = 'Unknown request'
            writer.write(HttpRequest.get_http_json_reply(state, http_code=HTTP_CODE_404_NOT_FOUND))
        else:
            handler = self.__routes[url]
            content_type = self.__content_types[url]

            status_code, content = handler(http_request.queries)

            writer.write(HttpRequest.get_http_header(http_code=status_code, content_type=content_type))
            writer.write('Access-Control-Allow-Origin: *\r\n')
            writer.write('\r\n')

            if content_type == CONTENT_TYPE_JSON:
                writer.write(json.dumps(content))
            else:
                writer.write(content)

        await writer.drain()
        await writer.wait_closed()
        print("Client disconnected")

    def create_async(self):
        return asyncio.start_server(lambda reader, writer: self.__handle_async(reader, writer), "0.0.0.0", self.__port)